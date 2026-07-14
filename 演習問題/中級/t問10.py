# 回答欄
file_list=["見積もり書_20230601_A.xlsx", "見積もり書_20231210_B.xlsx", "請求書_20230405.xlsx", "請求書_20231020.xlsx"]
#年月日の8桁の数字があればその8桁を取り出す
for file in file_list:
    for i in range(len(file)):
        if file[i] == "_":
            if file[i+1:i+9].isdigit():
                print(file[i+1:i+9])
                break