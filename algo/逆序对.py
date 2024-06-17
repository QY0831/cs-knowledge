# https://leetcode.cn/problems/count-of-smaller-numbers-after-self/description/
from sortedcontainers import SortedList
class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        n = len(nums)
        sl = SortedList([])
        ans = []
        for i in range(n - 1, -1, -1):
            j = sl.bisect_left(nums[i])
            sl.add(nums[i])
            ans.append(j)
        return ans[::-1]
    

# https://leetcode.cn/problems/reverse-pairs/description/
from sortedcontainers import SortedList
class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        sl = SortedList([])
        ans = 0
        n = len(nums)
        for i in range(n - 1, -1, -1):
            ans += sl.bisect_left(nums[i])
            sl.add(nums[i] * 2)
        return ans
    
