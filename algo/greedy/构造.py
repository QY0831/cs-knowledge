# 330, 2952完全一致，求最少添加的数目来取得[1, n]的所有数
# 1798是求最多能取得的连续数目

# https://leetcode.cn/problems/patching-array/
# 330. 按要求补齐数组
class Solution:
    def minPatches(self, nums: List[int], n: int) -> int:
        s = 1 # done [0, s)
        i = cnt = 0
        while s <= n:
            if i < len(nums) and nums[i] <= s: # merge [0, s) and [nums[i], s + nums[i])
                s += nums[i]
                i += 1
            else: # add s
                cnt += 1
                s *= 2
        return cnt


# https://leetcode.cn/problems/minimum-number-of-coins-to-be-added/description/
# 2952. 需要添加的硬币的最小数量
# rating: 1784
class Solution:
    def minimumAddedCoins(self, coins: List[int], target: int) -> int:
        coins.sort()
        s = 1 # 可取的开区间
        cnt = 0
        i = 0
        while s <= target:
            if i < len(coins) and coins[i] <= s: # merge [0, s-1] [x, s-1+x]
                s += coins[i]
                i += 1
            else: # add s
                cnt += 1
                s *= 2
        return cnt


# https://leetcode.cn/problems/maximum-number-of-consecutive-values-you-can-make/
# 1798. 你能构造出连续值的最大数目
# rating: 1931
class Solution:
    def getMaximumConsecutive(self, coins: List[int]) -> int:
        coins.sort()
        x = 0 # 目前能构造出的最大值
        for c in coins:
            if c > x + 1:
                return x + 1
            x += c # 0,1,2 +3 -> 3,4,5
        return x + 1

