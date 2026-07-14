#現在時刻を取得
import datetime
now = datetime.datetime.now()
print(now)
#現在時刻を表示
print(now.strftime("%Y/%m/%d %H:%M:%S"))
#1000分後の時刻を表示
after_1000_minutes = now + datetime.timedelta(minutes=1000)
print(after_1000_minutes.strftime("%Y/%m/%d %H:%M:%S"))