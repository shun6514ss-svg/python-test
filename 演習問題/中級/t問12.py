import random

#1から300までの数のの中で、その数を7で割った余りが0の数かつ奇数の数をlist_aに追加
list_a = []
for i in range(1, 301):
    if i%7==0 and i%2!=0:
        list_a.append(i)

#list_aの要素をランダムに並べ替えたlist_bを作成
list_b = list_a.copy()
random.shuffle(list_b)

#list_bを表示
print(list_b)