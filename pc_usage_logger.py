"""
Windows Event Log から「画面操作中」の時間を抽出する。

ロック解除〜ロックの間＝PCを操作中とみなす。
スリープ・スタンバイ中は含めない。

使用ログ:
  - Microsoft-Windows-Winlogon/Operational (812: ロック/解除)
  - Security (4800-4803: ロック/スクリーンセーバー) ※有効な場合
  - System (スリープ入出)
"""

import subprocess
import csv
import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict

LOOKBACK_DAYS = 90
OUTPUT_CSV = "pc_usage_log.csv"

# Winlogon Event フィールド: 4=ロック, 5=解除, 6=スクリーンセーバー開始, 7=終了
WINLOGON_ON = {"5", "7"}
WINLOGON_OFF = {"4", "6"}

SECURITY_ON = {4801, 4803}
SECURITY_OFF = {4800, 4802}

SLEEP_OFF = {42, 506, 109}
SHUTDOWN_OFF = {6006, 6008}


def classify_event(provider: str, event_id: int, winlogon_type: str | None = None) -> str | None:
    wt = str(winlogon_type) if winlogon_type is not None else ""
    if wt in WINLOGON_ON:
        return "on"
    if wt in WINLOGON_OFF:
        return "off"
    if event_id in SECURITY_ON:
        return "on"
    if event_id in SECURITY_OFF:
        return "off"
    if event_id in SLEEP_OFF:
        return "off"
    if event_id in SHUTDOWN_OFF:
        return "off"
    if provider == "Microsoft-Windows-Kernel-General" and event_id == 13:
        return "off"
    return None


def get_events_from_windows(lookback_days: int = LOOKBACK_DAYS) -> list[dict]:
    ps = f"""
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'
$start = (Get-Date).AddDays(-{lookback_days})
$result = @()

# Winlogon: ロック/解除（812のみ、SYSTEMユーザー除外）
try {{
    $wl = @(Get-WinEvent -LogName 'Microsoft-Windows-Winlogon/Operational' -MaxEvents 8000 |
        Where-Object {{ $_.TimeCreated -ge $start -and $_.Id -eq 812 }})
    foreach ($e in $wl) {{
        $xml = [xml]$e.ToXml()
        $wt = ($xml.Event.EventData.Data | Where-Object {{ $_.Name -eq 'Event' }}).'#text'
        $user = $xml.Event.System.Security.UserID
        if ($user -match 'S-1-5-18') {{ continue }}
        if ($wt -in @('4','5','6','7')) {{
            $result += [PSCustomObject]@{{
                Time = $e.TimeCreated.ToString('yyyy-MM-ddTHH:mm:ss')
                Id = $e.Id
                ProviderName = $e.ProviderName
                WinlogonType = [string]$wt
            }}
        }}
    }}
}} catch {{}}

# Security: ロック/スクリーンセーバー
$sec = @(Get-WinEvent -FilterHashtable @{{
    LogName='Security'; Id=4800,4801,4802,4803; StartTime=$start
}} -ErrorAction SilentlyContinue)
foreach ($e in $sec) {{
    $result += [PSCustomObject]@{{
        Time = $e.TimeCreated.ToString('yyyy-MM-ddTHH:mm:ss')
        Id = $e.Id
        ProviderName = $e.ProviderName
        WinlogonType = $null
    }}
}}

# System: スリープ
$all = @()
$all += @(Get-WinEvent -FilterHashtable @{{
    LogName='System'
    ProviderName='Microsoft-Windows-Kernel-Power'
    Id=42,506,109
    StartTime=$start
}} -ErrorAction SilentlyContinue)
$all += @(Get-WinEvent -FilterHashtable @{{
    LogName='System'; Id=6006,6008; StartTime=$start
}} -ErrorAction SilentlyContinue)
$all += @(Get-WinEvent -FilterHashtable @{{
    LogName='System'
    ProviderName='Microsoft-Windows-Kernel-General'
    Id=13
    StartTime=$start
}} -ErrorAction SilentlyContinue)

foreach ($e in $all) {{
    $result += [PSCustomObject]@{{
        Time = $e.TimeCreated.ToString('yyyy-MM-ddTHH:mm:ss')
        Id = $e.Id
        ProviderName = $e.ProviderName
        WinlogonType = $null
    }}
}}

if ($result.Count -eq 0) {{
    Write-Output '[]'
    exit 0
}}

$result |
    Sort-Object Time |
    ConvertTo-Json -Compress -Depth 3
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
    except Exception as e:
        print(f"Event Log 取得エラー: {e}")
        return []

    if result.stderr and result.stderr.strip():
        err = result.stderr.strip()
        if "No events were found" not in err:
            print(f"PowerShell警告: {err[:300]}")

    raw = (result.stdout or "").strip()
    if not raw:
        return []

    start = raw.find("[")
    start_obj = raw.find("{")
    if start == -1 and start_obj == -1:
        return []
    if start == -1 or (start_obj != -1 and start_obj < start):
        raw = raw[start_obj:]
        try:
            obj = json.loads(raw)
            return [obj] if isinstance(obj, dict) else []
        except json.JSONDecodeError:
            return []
    raw = raw[start:]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON 解析エラー: {e}")
        return []

    if isinstance(data, dict):
        return [data]
    return data if isinstance(data, list) else []


def parse_events(raw_events: list[dict]) -> list[tuple[datetime, str]]:
    timeline = []
    for ev in raw_events:
        try:
            time_str = ev.get("Time") or ""
            event_id = int(ev.get("Id"))
            provider = ev.get("ProviderName") or ""
            winlogon_type = ev.get("WinlogonType")
            kind = classify_event(provider, event_id, winlogon_type)
            if not kind:
                continue
            dt = datetime.strptime(time_str[:19], "%Y-%m-%dT%H:%M:%S")
            timeline.append((dt, kind))
        except Exception:
            continue

    # 同時刻は off を先に（ロック→解除の順を正しく）
    timeline.sort(key=lambda x: (x[0], 0 if x[1] == "off" else 1))

    simplified = []
    for dt, kind in timeline:
        if simplified and simplified[-1] == (dt, kind):
            continue
        simplified.append((dt, kind))
    return simplified


def add_session_to_daily(daily: dict, start: datetime, end: datetime) -> None:
    if end <= start:
        return

    current = start
    while current.date() <= end.date():
        day = current.date()
        day_end = datetime.combine(day, datetime.max.time())
        segment_end = min(end, day_end)
        hours = (segment_end - current).total_seconds() / 3600
        if hours > 0:
            daily[day] = min(24.0, daily[day] + hours)
        current = datetime.combine(day + timedelta(days=1), datetime.min.time())
        if current >= end:
            break


def calculate_daily_usage(
    timeline: list[tuple[datetime, str]],
    now: datetime | None = None,
) -> dict:
    """ロック解除〜ロックの間を日ごとに集計"""
    now = now or datetime.now()
    daily = defaultdict(float)
    session_start = None

    for dt, kind in timeline:
        if kind == "on":
            if session_start is None:
                session_start = dt
        elif kind == "off":
            if session_start is not None:
                add_session_to_daily(daily, session_start, dt)
                session_start = None

    # 最後のイベントが解除のまま → いままで操作中
    if session_start is not None and session_start <= now:
        add_session_to_daily(daily, session_start, now)

    return daily


def save_to_csv(daily_usage: dict, output_file: str = OUTPUT_CSV) -> None:
    if not daily_usage:
        print("集計するデータがありません")
        return

    sorted_dates = sorted(daily_usage.keys())
    start = sorted_dates[0]
    end = max(sorted_dates[-1], datetime.now().date())
    all_days = []
    d = start
    while d <= end:
        all_days.append(d)
        d += timedelta(days=1)

    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["日付", "使用時間（時間）", "使用時間（時:分）"])

            for day in all_days:
                hours = float(daily_usage.get(day, 0.0))
                hours_int = int(hours)
                minutes = int(round((hours - hours_int) * 60))
                if minutes == 60:
                    hours_int += 1
                    minutes = 0
                writer.writerow(
                    [day.strftime("%Y-%m-%d"), f"{hours:.2f}", f"{hours_int}:{minutes:02d}"]
                )

        used_days = sum(1 for day in all_days if daily_usage.get(day, 0) > 0)
        print(f"✓ CSVファイルが作成されました: {output_file}")
        print(f"✓ 集計期間: {start} ～ {end}")
        print(f"✓ 出力日数: {len(all_days)}日分（操作記録あり {used_days}日）")
    except Exception as e:
        print(f"CSVファイル保存エラー: {e}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("Windows Event Log から画面操作時間を抽出中...")
    print(f"   対象期間: 直近 {LOOKBACK_DAYS} 日")
    print("   集計方法: ロック解除〜ロック（スリープ・放置ロックは除外）")
    print()

    print("📊 ロック/解除・スリープイベントを取得中...")
    raw = get_events_from_windows(LOOKBACK_DAYS)
    print(f"   取得イベント数: {len(raw)}件")

    timeline = parse_events(raw)
    on_count = sum(1 for _, k in timeline if k == "on")
    off_count = sum(1 for _, k in timeline if k == "off")
    print(f"   操作開始(解除): {on_count}件 / 操作終了(ロック等): {off_count}件")

    if not timeline:
        print()
        print("イベントが見つかりませんでした")
        print("   Winlogon ログが無効の可能性があります")
        return

    now = datetime.now()
    print("📈 日ごとの画面操作時間を計算中...")
    daily_usage = calculate_daily_usage(timeline, now)

    print("💾 CSVファイルに保存中...")
    save_to_csv(daily_usage)

    if daily_usage:
        positive = {d: h for d, h in daily_usage.items() if h > 0}
        total_hours = sum(positive.values())
        avg_hours = total_hours / len(positive) if positive else 0
        print()
        print("=== サマリー（画面操作中・ログ抽出） ===")
        print(f"総操作時間: {total_hours:.2f}時間")
        print(f"平均操作時間: {avg_hours:.2f}時間/日（記録日のみ）")
        if positive:
            print(f"最大: {max(positive.values()):.2f}時間")
            print(f"最小: {min(positive.values()):.2f}時間")
            print(f"記録日数: {len(positive)}日")
        print()
        print("※ ロック解除〜ロックの間。キーボード操作そのものは記録されません")
        print("※ ロックせず放置した時間は含まれる場合があります")
        print()
        print("次: python pc_usage_graph.py でグラフ表示")


if __name__ == "__main__":
    main()
