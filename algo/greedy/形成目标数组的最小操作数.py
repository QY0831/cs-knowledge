# https://leetcode.cn/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/
# 1526. 形成目标数组的子数组最少增加次数
# 若target[i + 1] > target[i], target[i + 1]不会占用额外操作；
# 否则增加 target[i + 1] - target[i] 次操作。 
class Solution:
    def minNumberOperations(self, target: List[int]) -> int:
        ans = target[0]
        for a, b in pairwise(target):
            if b - a > 0:
                ans += b - a
        return ans
    
    
# https://leetcode.cn/problems/minimum-operations-to-make-array-equal-to-target/description/
# 3229. 使数组等于目标数组所需的最少操作次数
# 1526进阶版，根据正负号分段处理
class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        ans = abs(nums[0] - target[0])
        for (a, b), (c, d) in zip(pairwise(nums), pairwise(target)):
            d1 = a - c
            d2 = b - d
            if (d1 >= 0 and d2 >= 0) or (d1 <= 0 and d2 <= 0):
                # op don't change, can share
                if abs(d2) > abs(d1):
                    ans += abs(d2 - d1)
            else:
                # change op
                ans += abs(d2)
        return ans
