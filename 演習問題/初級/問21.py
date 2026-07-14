#今日の日付を取得
import datetime
today=datetime.date.today()
#-を/に変換
today=today.strftime("%Y/%m/%d")
print(today)