MOD = 1_000_000_007
MX = 100_000

# 100以内的质数
primes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]


# 埃氏筛求质数
MX = 10 ** 6 + 10
primes = []
is_prime = [True] * MX
is_prime[1] = False
for i in range(2, MX):
    if is_prime[i]:
        primes.append(i)
        for j in range(i * i, MX, i):
            is_prime[j] = False


# 直接判断是否是质数
def is_prime(n: int) -> bool:
    return all(n % i for i in range(2, isqrt(n) + 1))


# 预处理每个数的所有因子，时间复杂度 O(MlogM)，M=1e5
divisors = [[] for _ in range(MX)]
for i in range(1, MX):  
    for j in range(i, MX, i):
        divisors[j].append(i)


# 求一个数的所有质因数（没验证过）
def prime_factors(n):
    factors = []
    i = 2

    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    
    if n > 1:
        factors.append(n)
    
    return factors


# X里个选2个有多少种组合（不考虑顺序），c(x, 2)
def c2(x):
    return x * (x - 1) // 2

# 等差数列求和: 首相加末项处以项数除以2
def sum_arithmetic_seq(start, end, n):
    return (start + end) * n // 2

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

# 乘法原理
# https://leetcode.cn/problems/count-valid-paths-in-a-tree/
# https://leetcode.cn/problems/count-pairs-of-connectable-servers-in-a-weighted-tree-network
# 在统计树中能符合条件的点对时（它们位于不同的连通块）的方法：
# 设从0的邻居出发，能访问到3，4，5个符合条件的节点。
# 4和左边3个点，两两之间符合要求。
# 5和左边3+4个点，两两之间符合要求。
# 根据乘法原理，把4 * 3 + 5 * 7 加到答案中。


# 模运算
# a = k1*m + r1, b = k2*m + r2
# (a + b) mod m = (r1 + r2) mod m = (a mod m + b mod m) mod m


# 最小公倍数 lcm(Leatest Common Multiple)
lcm = math.lcm(d1, d2)
# 能被lcm的整除的，同时能被d1,d2整除

# 组合数：返回不重复且无顺序地从 n 项中选择 k 项的方式总数
math.comb(n, k)


# https://leetcode.cn/problems/find-the-number-of-good-pairs-ii/description/
# 求nums1[i] % (nums2[j] * k) == 0的个数
class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        cnt = Counter()
        for x in nums1:
            if x % k != 0:
                continue
            x //= k
            for d in range(1, isqrt(x) + 1): # x的因子
                if x % d != 0:
                    continue
                cnt[d] += 1
                if d * d < x:
                    cnt[x // d] += 1
        return sum(cnt[y] for y in nums2)
