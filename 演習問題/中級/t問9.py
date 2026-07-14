input_str=str(input("文字列を入力してください："))
#/の後に0がなかったら0を追加 全ての/の後に0を全て追加
for i in range(len(input_str)):
    if input_str[i] == "/":
        if input_str[i+1] != "0":
            input_str=input_str[:i+1]+"0"+input_str[i+1:]
print(input_str)