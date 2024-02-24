# X里个选2个有多少种组合（不考虑顺序），c(x, 2)
def c2(x):
    return x * (x - 1) // 2

# 等差数列求和: 首相加末项处以项数除以2
def sum_arithmetic_seq(start, end, n):
    return (start + end) * n // 2

