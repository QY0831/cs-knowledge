# 一维前缀和
pre = list(accumulate(arr, initial=0)) # sum[i, j] = pre[j+1] - pre[i]

