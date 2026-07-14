# 回答欄
List=["Apple", "Beautiful", "Teacher", "Lion", "Ocean", "Student", "Computer", "Amazon", "Python", "Phone"]
count=0
for list in List:
    for i in list:
        if i == "A" or i == "a":
            count+=1
            break
print(count)