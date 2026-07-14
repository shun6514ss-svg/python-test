# 回答欄
List=[52, 77, 24, 3, 31, 60, 86, 90, 35, 87, 55, 9, 79, 45, 73, 75, 30, 70, 59, 19]

# 差が最小となる組み合わせを探す
min_diff = float('inf')
result = None

for i in range(len(List)):
    for j in range(i+1, len(List)):
        diff = abs(List[i] - List[j])
        # 差が最小、または差が同じで和が最小
        if diff < min_diff or (diff == min_diff and List[i] + List[j] < result[0] + result[1]):
            min_diff = diff
            result = (List[i], List[j])
#二つの数の和を表示
print(result[0]+result[1])