# 每种物品的数量是无限的，要凑出体积amount
# 01 背包依赖的是「上一行正上方的格子」和「上一行左边的格子」
# 完全背包依赖的是「上一行正上方的格子」和「本行左边的格子」
# 空间优化时，内循环正序
# 
# https://leetcode.cn/problems/coin-change/description/
# 凑出amount的最少硬币数
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        f = [0] + [inf] * (amount)
        for c in coins:
            for x in range(c, amount + 1):
                f[x] = min(f[x], f[x - c] + 1)
        return f[-1] if f[-1] != inf else -1
    

# https://leetcode.cn/problems/coin-change-ii/description/
# 凑出amount的方案数
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        f = [1] + [0] * amount
        for c in coins:
            for x in range(c, amount + 1):
                f[x] += f[x - c]
        return f[-1]


# https://leetcode.cn/problems/combination-sum-iv/description
class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        # 无限选择物品 -> 完全背包 -> 内循环正向遍历
        # 求排列 -> 优先遍历背包
        dp = [0] * (target+1)
        dp[0] = 1
        n = len(nums)
        for i in range(1, target+1):  # 取得i个重量的方法数
            for j in range(n): 
                if i - nums[j] >= 0:
                    dp[i] += dp[i-nums[j]]
        return dp[target]

