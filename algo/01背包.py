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
                