input_text=str(input("文字列を入力してください："))
for i in range(len(input_text)):
    if input_text[i] == "a":
        print("はい")
        break
    else:
        print("いいえ")
        break