#inputで日付入力を受け取り、その日付の曜日を表示
import datetime
date = input("日付を入力してください: ")
date = datetime.datetime.strptime(date, "%Y/%m/%d")
#1234日前を表示
before_1234_days = date - datetime.timedelta(days=1234)
print(before_1234_days.strftime("1234日前は%Y/%m/%d"))
#曜日を表示
print(before_1234_days.strftime("1234日前は%A"))

