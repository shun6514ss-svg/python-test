input_number=int(input("数字を入力してください："))
for i in range(1, input_number+1):
    if input_number % i == 0:
        print(i)