# https://leetcode.cn/problems/maximum-strength-of-k-disjoint-subarrays/description/
# 计算划分的k个不相交子数组的最大能量和
# 能量和：x 个子数组的能量值： sum[1] * x - sum[2] * (x - 1) + sum[3] * (x - 2) - sum[4] * (x - 3) + ... + sum[x] * 1
# 其中 sum[i] 是第 i 个子数组的和
class Solution:
    def maximumStrength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        f = [[0] * (n + 1) for _ in range(k + 1)]
        for i in range(1, k + 1):
            f[i][i - 1] = mx = -inf
            w = (k - i + 1) * (1 if i % 2 else -1)
            # j 不能太小也不能太大，要给前面留 i-1 个数，后面留 k-i 个数
            for j in range(i, n - k + i + 1):
                mx = max(mx, f[i - 1][j - 1] - s[j - 1] * w)
                f[i][j] = max(f[i][j - 1], s[j] * w + mx)
        return f[k][n]


# https://leetcode.cn/problems/largest-sum-of-averages/description/
# 最多分成k个子数组，计算最大平均值和
class Solution:
    def largestSumOfAverages(self, nums: List[int], k: int) -> float:
        # f[i][j]: 前j个字符划分成i个子数组的最大平均值和
        # f[i][j]
        #   max( f[i-1][L] + s[L, j) / (j-L)  )
        s = list(accumulate(nums, initial=0))
        n = len(nums)
        f = [[0 for _ in range(n + 1)] for _ in range(k + 1)]
        for j in range(1, n + 1):
            f[1][j] = s[j] / j
        for i in range(2, k + 1):
            # 已划分i个，j后面还需要划分k - i个, j最多取n-k+i
            for j in range(i, n - k + i + 1):
                for L in range(i - 1, j):
                    f[i][j] = max(f[i][j], f[i-1][L] + (s[j] - s[L]) / (j - L))
        return f[k][n]


# https://leetcode.cn/problems/palindrome-partitioning-iii/
# 返回以将s分割成k个回文字符串所需修改的最少字符数
class Solution:
    def palindromePartition(self, s: str, k: int) -> int:
        
        @cache
        def get_op(i, j):
            if i >= j:
                return 0
            return int(s[i] != s[j]) + get_op(i + 1, j - 1)

        @cache
        def f(i, j): # 前i个，分j份
            if i <= 0:
                return 0
            if j == 1:
                return get_op(0, i - 1)
            res = inf
            for L in range(j - 1, i):
                res = min(res, f(L, j - 1) + get_op(L, i - 1))
            return res
        
        return f(len(s), k)


# 计算可划分的组数
# https://leetcode.cn/problems/minimum-substring-partition-of-equal-character-frequency/description/
class Solution:
    def minimumSubstringsInPartition(self, s: str) -> int:
        # f[i]: 前i个字符最少划分
        # f[i] = min(f[j] + 1 if s[j+1:i] is valid)
        n = len(s)
        f = [inf] * (n + 1)
        f[0] = 0
        for i in range(1, n + 1): # f[i]
            cnt = Counter()
            mx = c_cnt = 0  
            # 在s[j:i]
            # mx: 同一种字母最多出现几次； 
            # c_cnt：出现几种字母
            for j in range(i - 1, -1, -1): # f[j]
                cnt[s[j]] += 1
                if cnt[s[j]] == 1:
                    c_cnt += 1
                if cnt[s[j]] > mx:
                    mx = cnt[s[j]]

                if mx * c_cnt == i - j and f[j] + 1 < f[i]:
                    f[i] = f[j] + 1
        return f[-1]
