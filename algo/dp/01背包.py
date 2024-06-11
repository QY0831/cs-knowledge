# 关键词：子序列求和
# https://leetcode.cn/problems/find-the-sum-of-the-power-of-all-subsequences
class Solution:
    def sumOfPower(self, nums: List[int], k: int) -> int:
        MOD = 1_000_000_007
        n = len(nums)

        f = [[0 for _ in range(k + 1)] for _ in range(n + 1)]
        f[0][0] = 1
        for i in range(1, n + 1): # 前i个
            x = nums[i-1]
            for j in range(i, 0, -1): # 长度j
                for s in range(x, k + 1): # 合为s
                    f[j][s] = f[j-1][s-x] + f[j][s]
        ans = 0
        for j in range(1, n+1):
            substr_cnt = f[j][k]
            power = pow(2, n - j) * substr_cnt % MOD
            ans = (ans + power) % MOD
        return ans

# https://leetcode.cn/problems/length-of-the-longest-subsequence-that-sums-to-target
class Solution:
    def lengthOfLongestSubsequence(self, nums: List[int], target: int) -> int:
        # f[i][j]: 前i个字符和为j的子序列长度的最大值
        # f[i][j] = max(
        #   f[i-1][j],
        #   f[i-1][j-nums[i-1]] + 1   
        # )
        # 优化-> f[j] = max(f[j], f[j-nums[i-1]] + 1)，内循环逆序
        n = len(nums) 
        f = [-1 for _ in range(target + 1)] # -1代表取不到
        f[0] = 0
        for i in range(1, n + 1):
            x = nums[i - 1]
            for j in range(target, x - 1, -1):
                f[j] = max(f[j], f[j - x] + 1 if f[j - x] != -1 else -1)
        return f[-1]

# bitset优化01背包问题
# https://leetcode.cn/problems/maximum-total-reward-using-operations-ii
# 周赛401 T4
class Solution:
    def maxTotalReward(self, rewardValues: List[int]) -> int:
        nums = sorted(set(rewardValues))
        # f[i][j]: 能否从前i个数得到奖励j, j的上限：2 * max(nums)
        # f[i][j] = f[i-1][j]
        # f[i][j] = f[i-1][j-nums[i]] if j >= nums[i] and nums[i] > j - nums[i] -> nums[i] <= j <= 2 * nums[i]
        # f[i][j] = f[i-1][j] or f[i-1][j-nums[i]]
        # 去掉一个维度：
        # v = nums[i]
        # f[j] |= f[j-v], 0 <= j - v < v
        # 用一个二进制数f保存状态，（f的第j位为1）== （f[j]=True），即奖励j能取到
        # (1 << v) - 1 表示所有小于v的值
        # f & ((1 << v) - 1) 表示能取到的f[j-v]
        # << v 表示加上v, 得到了能得到的新的数
        # f最高位的1的位数即为能取到的最大值
        f = 1 # 表示f[0]=1
        for v in nums:
            f |= (f & ((1 << v) - 1)) << v
        return f.bit_length() - 1
    
# 优化思想：在一些要求相邻状态不同的DP问题中，在处理当前状态时，不一定非要与所有前置状态比较，只需要记录dp最大和次大值对应的前置状态即可。
# https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-ii/description/
class Solution:
    def maximumLength(self, nums: List[int], k: int) -> int:
        # f[i][j]: 以nums[i]结尾，且有j个相邻不想等元素的子序列的最大长度
        # f[i][j] = max( f[i'][j] + 1 if nums[i] == nums[i'] else f[i'][j-1] + 1 ), i' < i
        # 由于转移时，只需考虑 nums[i] == nums[i']，
        # 无需尝试所有的i'，可以记录以数字x结尾，且有j个相邻不想等元素的最大长度： f[x][j]
        # f[x][j] = max(f[x][j], f[x'][j-1]) + 1
        # 为了知道最大的f[x'][j-1]，需要维护f[x'][j-1]中的最大值mx, 无需考虑x'!=x，因为f[x][j]>f[x-1][j]
        f = [0] * (k + 1) # f[i][j] 滚动数组 
        cnt = [defaultdict(int) for _ in range(k + 1)] # cnt[kk][x] 以x结尾用了k次的最长子序列
        for x in nums:
            for kk in range(k, -1, -1):
                cnt[kk][x] = max(cnt[kk][x], f[kk - 1] if kk > 0 else 0) + 1
                f[kk] = max(f[kk], cnt[kk][x])
        return f[-1]
