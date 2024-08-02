# https://leetcode.cn/problems/count-alternating-subarrays/
# 3101. 交替子数组计数
# rating: 1404
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


# 2134. 最少交换次数来组合所有的 1 II
# https://leetcode.cn/problems/minimum-swaps-to-group-all-1s-together-ii/description/
# rating: 1748
# 将数组中的所有 1 聚集在一起需要的最少交换次数。
# 算法：滑动窗口
class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        n = len(nums)
        left = right = 0
        ones = sum(nums)
        zeros = n - ones
        mx1 = mx0 = cnt1 = cnt0 = 0
        while right < n:
            cnt1 += nums[right]
            right += 1
            if right - left > ones:
                cnt1 -= nums[left]
                left += 1
            if cnt1 > mx1:
                mx1 = cnt1

        left = right = 0
        while right < n:
            if nums[right] == 0:
                cnt0 += 1
            right += 1
            if right - left > zeros:
                if nums[left] == 0:
                    cnt0 -= 1
                left += 1
            if cnt0 > mx0:
                mx0 = cnt0
        
        return min(ones - mx1, zeros - mx0)
