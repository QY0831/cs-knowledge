mod = 10**9 + 7
# 快速幂求出 x^y % mod
# 递归
def qpow(x: int, y: int) -> int:
    if y == 0:
        return 1
    elif y % 2 == 1:
        return qpow(x, y - 1) * x
    else:
        tmp = qpow(x, y // 2)
        return tmp * tmp

# 非递归
def qpow(x: int, y: int) -> int:
    ret, mul = 1, x
    while y > 0:
        if y % 2 == 1:
            ret = ret * mul % mod
        mul = mul * mul % mod
        y //= 2
    return ret
