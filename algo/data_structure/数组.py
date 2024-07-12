# O(n) 找到一段连续的值为target, 大小为size的子数组
arr = [3, 3, 1, 1, 1, 0]
cnt = 0
target = 1
size = 3
for i, x in enumerate(arr):
    if x != target:
        cnt = 0
    else:
        cnt += 1
        if cnt == size:
            # found
            break
