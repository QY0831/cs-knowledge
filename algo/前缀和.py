# 一维前缀和
pre = list(accumulate(arr, initial=0)) # sum[i, j] = pre[j+1] - pre[i]

# 二维前缀和
m = len(grid)
n = len(grid[0])
pre_sum = [[0] * (n+1) for _ in range(m+1)]
ans = 0
for i in range(1, m+1):
    for j in range(1, n+1):
        pre_sum[i][j] = pre_sum[i-1][j] + pre_sum[i][j-1] - pre_sum[i-1][j-1] + grid[i-1][j-1]