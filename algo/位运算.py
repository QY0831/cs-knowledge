# low-bit: 得到最低位的1（2次幂）
while n:
    lb = n & -n
    n ^= lb


# 2的整数次幂满足
i & (i - 1) == 0

