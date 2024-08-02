# https://leetcode.cn/problems/largest-rectangle-in-histogram/
# 最大矩形面积
# 单调栈：找左侧、右侧的更小元素的位置
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


# https://leetcode.cn/problems/maximal-rectangle/
# 最大矩形
# 逐行处理，生成heights，将问题转化为上一题 https://leetcode.cn/problems/largest-rectangle-in-histogram/
class Solution:
    
    def solve(self, heights):
        heights = [0] + heights + [0]
        stk = []
        res = 0
        for i, h in enumerate(heights):
            while stk and h < heights[stk[-1]]:
                 j = stk.pop() # height
                 k = stk[-1] # left bound
                 width = i - k - 1
                 res = max(res, width * heights[j])
            stk.append(i)
        return res
                 
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix:
            return 0
        m = len(matrix)
        n = len(matrix[0])
        heights = [0] * n
        ans = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    heights[j] += 1
                else:
                    heights[j] = 0
            ans = max(ans, self.solve(heights))
        return ans
    

# https://leetcode.cn/problems/largest-submatrix-with-rearrangements/
# 重新排列column后的最大矩形面积
# 预处理每一列的height，逐行计算
class Solution:
    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        m = len(matrix)
        n = len(matrix[0])
        for j in range(n):
            for i in range(1, m):
                if matrix[i][j] == 1:
                    matrix[i][j] += matrix[i-1][j]
        ans = 0
        for i in range(m):
            matrix[i].sort()
            for j in range(n - 1, -1, -1):
                ans = max(ans, matrix[i][j] * (n - j))
        return ans


# https://leetcode.cn/problems/minimum-area-rectangle/description/
# 939. 最小面积矩形
# rating: 1752
# 给出点集，求最小面积矩形
# 解法：按x轴排序，对于每个x，按y轴排序，遍历(y1, y2)，查看之前是否有相同的y，计算面积
class Solution:
    def minAreaRect(self, points: List[List[int]]) -> int:
        cols = defaultdict(list)
        for x, y in points:
            cols[x].append(y)
        ans = inf
        pre = dict() # key: y1, y2 val: x
        for x in sorted(cols):
            col = cols[x]
            col.sort()
            for j, y2 in enumerate(col):
                for i in range(j):
                    y1 = col[i]
                    if (y1, y2) in pre:
                        prex = pre[(y1, y2)]
                        ans = min(ans, (y2 - y1) * (x - prex))
                    pre[(y1, y2)] = x
        return ans if ans != inf else 0
