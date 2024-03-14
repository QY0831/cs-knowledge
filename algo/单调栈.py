# 求最大坡 i < j and A[i] <= A[j]
def maxWidthRamp(nums: List[int]) -> int:
    ans = 0
    stack = []
    for i, v in enumerate(nums):
        if not stack or v < nums[stack[-1]]:
            stack.append(i)
    
    for i in range(len(nums) - 1, -1, -1):
        while stack and nums[i] >= nums[stack[-1]]:
            j = stack.pop()
            ans = max(ans, i - j)
    return ans


# 对i位置上一个更大元素距离当前有多远
# 单调递减栈 - 对于当前nums[i]，栈内无需保存比nums[i]更小的nums[j](j < i)，因为i永远比j适合作为后面元素的答案
# https://leetcode.cn/problems/online-stock-span/description/
class StockSpanner:

    # 单调递减栈
    def __init__(self):
        self.stack = [(-1, inf)]
        self.day = -1

    def next(self, price: int) -> int:
        while price >= self.stack[-1][1]:# 把小于当前price的都pop掉，堆顶天数后一天到今天即为答案
            self.stack.pop()
        self.day += 1
        ans =  self.day - self.stack[-1][0]
        self.stack.append((self.day, price))
        return ans
    
