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



# 单调递减栈求最长j-i满足 i < j and nums[i] > nums[j]
# https://leetcode.cn/problems/longest-well-performing-interval/description/
class Solution:
    def longestWPI(self, hours: List[int]) -> int:
        n = len(hours)
        pre = [0]
        t = 0
        for i, x in enumerate(hours):
            pre.append(pre[-1] + 1 if x > 8 else pre[-1] - 1)
        # 9 9 6 0 6 6 9
        # pre[i] -> 0~i-1天 劳累-休闲 天数
        # pre[j] - pre[i] > 0 -> i~j-1天是劳累的
        # 在pre数组找最长的一段，满足pre[j]-pre[i]>0，答案为j-i

        # 对于pre中的左端点，可以用单调递减栈保存
        # j > i, 只有 nums[j] < nums[i] 时，j 才可能是比 i 更优的左端点
        stk = [0]
        for i, x in enumerate(pre):
            if x < pre[stk[-1]]:
                stk.append(i)
        # 倒叙遍历pre, 找到大于栈顶的值，即为最长
        ans = 0
        for i in range(n, 0, -1):
            while stk and pre[i] > pre[stk[-1]]:
                ans = max(ans, i - stk.pop())
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


# https://leetcode.cn/problems/largest-rectangle-in-histogram/
# 最大矩形面积
# 单调栈：找左侧、右侧的更小元素的位置(可跳过中间的更大元素)
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        # 每个高度h，找到左、右侧最近的高度小于h的柱子
        n = len(heights)
        stk = [] # 单调递增
        pre = []
        for i, h in enumerate(heights):
            while stk and h <= heights[stk[-1]]:
                stk.pop()
            if stk:
                pre.append(stk[-1]) # 栈顶就是<且最近的柱子
            else:
                pre.append(-1) 
            stk.append(i)
        
        stk = []
        suf = []
        for i in range(n - 1, -1, -1):
            h = heights[i]
            while stk and h <= heights[stk[-1]]:
                stk.pop()
            if stk:
                suf.append(stk[-1])
            else:
                suf.append(n)
            stk.append(i)

        ans = 0
        for i in range(n):
            s = (suf[n - 1 - i] - pre[i] - 1) * heights[i]
            ans = max(s, ans)
        return ans


# https://leetcode.cn/problems/maximum-subarray-min-product/description/
# 1856. 子数组最小乘积的最大值
# rating: 2051
# 目的：求以nums[i]为最小值的子数组的最大乘积 -> 求该子数组左侧、右侧边界 -> 单调递增栈
class Solution:
    def maxSumMinProduct(self, nums: List[int]) -> int:
        n = len(nums)
        stk = [] # 单调递增求下一个更小元素
        left = [-1] * n
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stk and x < nums[stk[-1]]:
                left[stk.pop()] = i
            stk.append(i)

        stk = []
        right = [n] * n
        for i in range(n):
            x = nums[i]
            while stk and x < nums[stk[-1]]:
                right[stk.pop()] = i
            stk.append(i)

        pre = list(accumulate(nums, initial=0)) 
        # sum[i, j] = pre[j+1] - pre[i]
        # sum(i, j) = pre[j] - pre[i+1]

        ans = 0
        for i in range(n):
            l, r = left[i], right[i]
            # 求sum (left ... right)
            ans = max(ans, (pre[r] - pre[l+1]) * nums[i])
        return ans % 1_000_000_007
