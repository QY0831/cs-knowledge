# LEETCODE https://leetcode.cn/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/description/
class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        n = len(nums)
        d1 = deque([]) # 单调递增保存最小值
        d2 = deque([]) # 单调递减保存最大值
        left = right = 0
        while right < n:
            v = nums[right]
            while d1 and nums[d1[-1]] > v:
                d1.pop()
            while d2 and nums[d2[-1]] < v:
                d2.pop()
            d1.append(right)
            d2.append(right)
            # 压缩左边界以满足条件
            while nums[d2[0]] - nums[d1[0]] > limit:
                left += 1
                if d2[0] < left:
                    d2.popleft()
                if d1[0] < left:
                    d1.popleft()
            ans = max(ans, right - left + 1)
        return ans