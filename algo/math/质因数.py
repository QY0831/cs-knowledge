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
    return all(n % i for i in range(2, isqrt(n) + 1)) # isqrt 平方根向下取整


# 预处理每个数的所有因子，时间复杂度 O(MlogM)，M=1e5
divisors = [[] for _ in range(MX)]
for i in range(1, MX):  
    for j in range(i, MX, i):
        divisors[j].append(i)
        

# 模运算
# a = k1*m + r1, b = k2*m + r2
# (a + b) mod m = (r1 + r2) mod m = (a mod m + b mod m) mod m


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


# https://leetcode.cn/problems/count-pairs-that-form-a-complete-day-ii/description/
# 求 (nums[i] + nums[j]) % 24 = 0 的组合数
class Solution:
    def countCompleteDayPairs(self, hours: List[int]) -> int:
        ans = 0
        cnt = [0] * 24
        for t in hours:
            ans += cnt[(24 - t % 24) % 24]
            cnt[t % 24] += 1
        return ans


# https://leetcode.cn/problems/find-the-count-of-numbers-which-are-not-special/description/
# 3233. 统计不是特殊数字的数字数量
# 只有两个真因数（除本身外的因子）的数是特殊数字，求[l, r]中不是特殊数字的个数
# 解法：筛质数，质数的平方是特殊数字, 统计[sqrt(l), sqrt(r)]中的质数个数
class Solution:
    def nonSpecialCount(self, l: int, r: int) -> int:
        ls, rs = ceil(sqrt(l)), isqrt(r)
        MX = rs + 10
        is_prime = [True] * MX
        is_prime[1] = False
        for i in range(2, MX):
            if is_prime[i]:
                for j in range(i * i, MX, i):
                    is_prime[j] = False

        cnt = 0
        for i in range(ls, rs + 1):
            if is_prime[i]:
                cnt += 1

        return r - l + 1 - cnt
