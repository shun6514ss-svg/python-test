input_text=str(input("文字列を入力してください："))
#aとbが両方含まれている場合
if "a" in input_text and "b" in input_text:
    print("both")
#aが含まれている場合
elif "a" in input_text:
    print("yes")
#aとbが両方含まれていない場合
else:
    print("no")