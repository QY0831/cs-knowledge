# https://leetcode.cn/problems/count-alternating-subarrays/
# 3101. 交替子数组计数
# 难度：1404
# 如果一个子数组中不存在两个相邻元素的值相同的情况，我们称这样的子数组为交替子数组 。
class Solution:
    def countAlternatingSubarrays(self, nums: List[int]) -> int:
        ans = 0
        left = 0
        for right in range(len(nums)):
            if right > 0 and nums[right] == nums[right - 1]:
                left = right
            ans += right - left + 1 # 以right为右端点的答案数
        return ans
    
    
# https://leetcode.cn/problems/alternating-groups-ii/
# 3208. 交替组 II
class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], k: int) -> int:
        n = len(colors)
        ans = cnt = 0
        # cnt: 交替子数组的长度
        for i in range(2 * n):
            if i > 0 and colors[i % n] == colors[(i - 1) % n]:
                cnt = 0
            cnt += 1
            if i >= n and cnt >= k:
                ans += 1
        return ans
