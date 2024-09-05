# 计算划分个数
# 计算最少（最多）可以划分的子数组个数、方案数等。
# 一般定义f[i]表示前缀a[:i]在约束下，分割出最少（最多）的子数组个数
# 枚举最后一个子数组的左端点L, 从f[L]转移到f[i]，并考虑a[L:j]对最优解的影响。

# https://leetcode.cn/problems/partition-string-into-minimum-beautiful-substrings/
# 2767. 将字符串分割为最少的美丽子字符串
ss = set()
MX = 1 << 16
i = 0
while True:
    x = pow(5, i)
    if x > MX:
        break
    ss.add(bin(x)[2:])
    i += 1

class Solution:
    def minimumBeautifulSubstrings(self, s: str) -> int:
        n = len(s)
        f = [inf] * (n + 1)
        f[0] = 0
        for i in range(1, n + 1):
            for L in range(i):
                if s[L] != '0' and f[L] != inf and s[L:i] in ss:
                    f[i] = min(f[i], f[L] + 1)
        return f[-1] if f[-1] != inf else -1
    

# https://leetcode.cn/problems/filling-bookcase-shelves/description/
# 1105. 填充书架
class Solution:
    def minHeightShelves(self, books: List[List[int]], shelfWidth: int) -> int:
        n = len(books)
        f = [inf] * (n + 1)
        f[0] = 0
        for i in range(1, n + 1):
            t, h = books[i - 1]
            sum_width = t
            max_h = h
            f[i] = f[i - 1] + h
            for L in range(i - 2, -1, -1):
                # [L:i]的书放在一层
                t, h = books[L]
                if h > max_h: 
                    max_h = h
                sum_width += t
                if sum_width > shelfWidth:
                    break
                if f[L] + max_h < f[i]:
                    f[i] = f[L] + max_h
        return f[-1]



# 约束划分个数
# 将数组分成（恰好/至多）k 个连续子数组，计算与这些子数组有关的最优值。
# 一般定义 f[i][j] 表示将长为 j 的前缀 a[:j] 分成 i 个连续子数组所得到的最优解。

# https://leetcode.cn/problems/maximum-strength-of-k-disjoint-subarrays/description/
# 3077. K 个不相交子数组的最大能量值
# rating: 2556
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
# 813. 最大平均值和的分组
# rating: 1936
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
# 1278. 分割回文串 III
# rating: 1979
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


# https://leetcode.cn/problems/allocate-mailboxes/
# 1478. 安排邮筒
# rating: 2190
class Solution:
    def minDistance(self, houses: List[int], k: int) -> int:
        # cost[i][j]: 在house[i],house[j]间放一个邮筒的最小总花费，放在中位数处总和最小
        # 1 4 8 9 20
        # med = 8
        # 4 8 9
        # med = 8
        # cost[i][j] = cost[i+1][j-1] + house[j] - house[i]
        n = len(houses)
        houses.sort()
        cost = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n): # j > i
                if i == j:
                    cost[i][j] = 0
                else:
                    cost[i][j] = cost[i+1][j-1] + houses[j] - houses[i]
        
        # f[i][j]: 前i个房子，放j个邮筒的最小距离和
        # f[i][j] = min(f[L][j-1] + cost[L][i], L:[0,i-1], j:[2, min(i+1, k)])
        f = [[inf] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 0
        for i in range(1, n + 1):
            f[i][1] = cost[0][i - 1]
            for j in range(2, min(i+1, k) + 1):
                for L in range(i):
                    if f[L][j-1] != inf:
                        f[i][j] = min(f[i][j], f[L][j-1] + cost[L][i-1])
        return f[-1][-1]


# 不相交区间
# 给定 n 个闭区间 [left_i,right_i,score_i].
# 请你在数轴上选择若干区间,使得选中的区间之间互不相交.
# 返回可选取区间的最大权值和.

# https://leetcode.cn/problems/maximize-the-profit-as-the-salesman/
# 2830. 销售利润最大化
# rating: 1851
class Solution:
    def maximizeTheProfit(self, n: int, offers: List[List[int]]) -> int:
        # f[i]: 前i个房屋能赚取的最大金币
        # 不买第i个：f[i] = f[i-1] 
        # 买第i个：f[i] = f[i0] + g0 if j0 == i - 1，遍历所有end == i - 1的offer来更新f[i]
        mp = defaultdict(list)
        for s, e, g in offers:
            mp[e].append((s, g))
        f = [0] * (n + 1)
        for end in range(1, n + 1):
            f[end] = f[end - 1]
            for s, g in mp[end - 1]:
                f[end] = max(f[end], f[s] + g)
        return f[-1]


# https://leetcode-cn.com/problems/maximum-profit-in-job-scheduling/
# 1235. 规划兼职工作
# rating: 2022
class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))  # 按照结束时间排序
        f = [0] * (len(jobs) + 1)
        for i, (_, st, p) in enumerate(jobs):
            j = bisect_left(jobs, (st + 1,), hi=i) 
            # 比当前job结束时间早的end最大的job -> 找 end[j] >= st + 1 则 end[j-1] < st + 1 -> end[j-1] <= st, 对应f[j]
            f[i + 1] = max(f[i], f[j] + p)
        return f[-1]


# https://leetcode.cn/problems/maximum-number-of-events-that-can-be-attended-ii/description/
# 1751. 最多可以参加的会议数目 II
# rating: 2040
# 比1235多一个维度，且start, end不能重合
class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events = sorted((e, s, v) for s, e, v in events)  # 按照结束时间排序
        n = len(events)
        f = [[0] * (k+1) for _ in range(n + 1)]
        for i, (_, s, v) in enumerate(events):
            j = bisect_left(events, (s, ), hi=i) # end[j] >= s  -> end[j-1] < s 
            for kk in range(1, k + 1):
                f[i + 1][kk] = max(f[i][kk], f[j][kk - 1] + v)
        return f[-1][-1]