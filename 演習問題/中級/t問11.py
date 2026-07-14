# 回答欄
text="Python is a versatile, high-level, interpreted language known for simple syntax, object-oriented programming, a large standard library, and applications in various fields, with a strong developer community and easy-to-read code."
#textをリストに変換
text_list=text.split()
#冠詞のaをtheに変換
new_list = []
for word in text_list:
    if word == "a":
        word = "the"
    new_list.append(word)
text=" ".join(new_list)
print(text)