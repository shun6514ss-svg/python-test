import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['Yu Gothic', 'MS Gothic', 'Meiryo', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11

csv_file = 'pc_usage_log.csv'

if not os.path.exists(csv_file):
    print(f"❌ ファイルが見つかりません: {csv_file}")
    print("   先に pc_usage_logger.py を実行してください")
    exit(1)

try:
    df = pd.read_csv(csv_file, encoding='utf-8')
    print(f"✓ ファイル読み込み完了: {len(df)}日分のデータ")
except Exception as e:
    print(f"❌ ファイル読み込みエラー: {e}")
    exit(1)

if '日付' in df.columns:
    df['date'] = pd.to_datetime(df['日付'])
    df['usage_hours'] = df['使用時間（時間）'].astype(float)
else:
    print("❌ CSVファイルのカラム名が異なります")
    print(f"   現在のカラム: {list(df.columns)}")
    exit(1)

DISPLAY_DAYS = 30
end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
start_date = end_date - timedelta(days=DISPLAY_DAYS - 1)
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

df = (
    df.set_index('date')[['usage_hours']]
    .groupby(level=0).sum()
    .reindex(all_dates, fill_value=0.0)
    .rename_axis('date')
    .reset_index()
)

recorded_days = int((df['usage_hours'] > 0).sum())
print(f"✓ 表示範囲: {start_date.date()} ～ {end_date.date()}（{DISPLAY_DAYS}日分・記録あり {recorded_days}日）")

if recorded_days == 0:
    print("❌ 過去30日間に使用時間の記録がありません")
    exit(1)

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f5f5f5'

num_days = len(df)
date_labels = [f"{d.month}/{d.day}" for d in df['date']]
hours = [float(h) for h in df['usage_hours'].tolist()]
avg_hours = float(df.loc[df['usage_hours'] > 0, 'usage_hours'].mean())
y_max = max(hours) if max(hours) > 0 else 1

# 縦棒グラフ：下=日付、左=時間 右上に注釈　橙色：平均以下　紫色：平均以上　灰色：0
fig_width = max(14, 0.7* num_days)
fig, ax = plt.subplots(figsize=(fig_width, 8))
ax.set_title('画面操作中の時間（ログ抽出）紫：平均以上 橙：平均以下', fontsize=18, pad=16)

x_pos = list(range(num_days))
colors = ['#A23B72' if h >= avg_hours and h > 0 else '#F18F01' if h > 0 else '#d0d0d0'
          for h in hours]

bars = ax.bar(x_pos, hours, color=colors, alpha=0.85,
              edgecolor='black', linewidth=0.4, width=0.75)
ax.axhline(y=avg_hours, color='red', linestyle='--',
           linewidth=2.0, label=f'平均: {avg_hours:.1f}h', zorder=5)

# 横軸（下）: 日付
ax.set_xticks(x_pos)
ax.set_xticklabels(date_labels, rotation=0, ha='center', fontsize=9)
ax.set_xlabel('日付（月/日）', fontsize=13)
ax.set_xlim(-0.5, num_days - 0.5)
ax.tick_params(axis='x', labelsize=9)

# 縦軸（左）: 使用時間
ax.set_ylabel('画面操作時間（時間）', fontsize=13)
ax.set_ylim(0, y_max * 1.22)
ax.set_yticks(list(range(0, int(y_max) + 2, 1)))
ax.tick_params(axis='y', labelsize=10)
ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# 棒の上に時間を表示
for bar, h in zip(bars, hours):
    if h > 0:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + y_max * 0.02,
            f'{h:.1f}h',
            ha='center', va='bottom',
            fontsize=9, color='#1a1a1a',
            zorder=4,
        )

ax.legend(fontsize=11, loc='upper right')
plt.tight_layout()
plt.subplots_adjust(bottom=0.18)

print("\n" + "=" * 60)
print("Statistics")
print("=" * 60)
print(f"Period: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Total usage: {df['usage_hours'].sum():.2f} hours")
print(f"Average (recorded days): {avg_hours:.2f} hours/day")
print(f"Recorded days: {recorded_days} / {DISPLAY_DAYS}")
idx_max = df['usage_hours'].idxmax()
print(f"Max usage: {df.loc[idx_max, 'usage_hours']:.2f} hours ({df.loc[idx_max, 'date'].date()})")
print("=" * 60)

import matplotlib

output_file = 'pc_usage_graph.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight', format='png')
print(f"\nGraph saved: {output_file}")

if matplotlib.get_backend().lower() != 'agg':
    try:
        plt.show()
    except KeyboardInterrupt:
        print("グラフ表示を終了しました")
