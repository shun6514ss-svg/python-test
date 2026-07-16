# PC使用時間ログ集計ツール

Windows PCの毎日の使用時間をEvent Logから取得し、CSVファイルで出力するツールです。

## 機能

- Windows Event Logから起動・シャットダウンイベントを自動取得
- 日ごとのPC使用時間を計算・集計
- CSV形式でレポートを出力
- 合計、平均、最大、最小使用時間を表示

## 要件

- Windows 10/11
- Python 3.6以上
- 管理者権限（Event Log読み取り用）

## インストール

### 1. 必要なパッケージをインストール

**方法A：バッチファイルを使用（最も簡単）**
```bash
setup.bat
```

**方法B：コマンドプロンプトで手動インストール**
```bash
pip install pandas matplotlib japanize_matplotlib
```

## 使い方

### 🚀 最も簡単：全自動実行

ログ取得とグラフ生成をまとめて実行：

**方法A：バッチファイル（Windows GUI）**
```bash
run_all.bat
```
フォルダから `run_all.bat` をダブルクリック

**方法B：PowerShell（自動管理者昇格）**
```powershell
.\run_all.ps1
```

**方法C：コマンドプロンプト**
```bash
python run_all.py
```

---

### 📋 個別実行

#### 1. ログ取得のみ
```bash
python pc_usage_logger.py
```

#### 2. グラフ表示のみ
```bash
python pc_usage_graph.py
```

#### 3. グラフ表示（英語版）
```bash
python pc_usage_graph_en.py
```

---

### 3. 出力ファイル

実行後、カレントディレクトリに `pc_usage_log.csv` が生成されます。

**CSVフォーマット:**
```
日付,使用時間（時間）,使用時間（時:分）
2024-01-15,8.50,8:30
2024-01-16,9.25,9:15
2024-01-17,7.75,7:45
```

## トラブルシューティング

### 「イベントが見つかりませんでした」と出る

- Event Logに起動・シャットダウン記録がない可能性があります
- 管理者権限で実行してください
- Windows Event Logの保持期間を確認してください（デフォルト7日）

### 権限エラー

- コマンドプロンプトを管理者として実行してから、スクリプトを実行してください

## カスタマイズ

### 出力ファイル名を変更

`pc_usage_logger.py` の最後の行を修正：

```python
save_to_csv(daily_usage, output_file="custom_filename.csv")
```

### 特定期間のデータを取得

`get_event_log_events()` 関数のPowerShellコマンドに `-After` パラメータを追加：

```powershell
-After (Get-Date).AddDays(-30)  # 過去30日間
```

## 注意事項

- Event Logのデータは通常7日間保持されます
- より古いデータが必要な場合は、Event Logの保持ポリシーを変更してください
- このツールはシステムイベントのみを読み取り、個人データは収集しません
