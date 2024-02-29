# X里个选2个有多少种组合（不考虑顺序），c(x, 2)
def c2(x):
    return x * (x - 1) // 2

# 等差数列求和: 首相加末项处以项数除以2
def sum_arithmetic_seq(start, end, n):
    return (start + end) * n // 2


MOD = 1_000_000_007
MX = 100_000

# 组合数模板
fac = [0] * MX # 阶乘
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i - 1] * i % MOD

inv_fac = [0] * MX # 阶乘的逆元
inv_fac[MX - 1] = pow(fac[MX - 1], -1, MOD)
for i in range(MX - 1, 0, -1):
    inv_fac[i - 1] = inv_fac[i] * i % MOD

def comb(n: int, k: int) -> int: # n个里选k个
    return fac[n] * inv_fac[k] % MOD * inv_fac[n - k] % MOD