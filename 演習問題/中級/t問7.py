input_text=str(input("文字列を入力してください："))
input_text_list=list(input_text)
input_text_list.reverse()
input_text_list="".join(input_text_list)
if input_text == input_text_list:
    print("はい")
else:
    print("いいえ")