# 初始化差分
n = len(nums)
d = [0] * (n + 1)
d[0] = nums[0]
for i in range(1, n):
    d[i] = nums[i] - nums[i-1]

# 差分数组还原原数组
arr = []
cur = 0
for x in d:
    cur += x
    arr.append(cur)
    
# 对数组a中连续子数组的操作，可以转变成对差分数组中两个数的操作
# 把 a[i],a[i+1] ... a[j] 加上 x
# 等价于将 d[i]+x, d[j+1]-x
