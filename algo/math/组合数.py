# 无重复数组的组合数
from math import factorial
factorial(6) # 6! = 720

# 有重复数字的组合数
# https://leetcode.cn/problems/find-the-count-of-good-integers/
# 3272. 统计好整数的数目
class Solution:
    def countGoodIntegers(self, n: int, k: int) -> int:
        if n == 1:
            return sum(x % k == 0 for x in range(1, 10))

        # 枚举回文左半边
        res = set()
        if n % 2:
            d = (n - 1) // 2
        else:
            d = n // 2

        start = pow(10, d - 1)
        end = pow(10, d)
        for num in range(start, end):
            l = str(num)
            r = l[::-1]
            if n % 2:
                for m in range(10):
                    s = l + str(m) + r
                    if int(s) % k == 0:
                        res.add(''.join(sorted(s)))
            else:
                s = l + r
                if int(s) % k == 0:
                    res.add(''.join(sorted(s)))

        fac = [factorial(i) for i in range(n + 1)]
        ans = 0
        for s in res:
            cnt = Counter(s)
            res = (n - cnt['0']) * fac[n-1] # 不考虑重复的，第一个数有 n - cnt['0']个可能性，其次(n - 1) * (n - 2) ... 1
            # 去重
            for c in cnt.values():
                res //= fac[c] # 除以重复数字的排列数
            ans += res
        return ans
