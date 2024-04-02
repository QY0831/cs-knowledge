# 矩形重叠面积
class Solution:
    def computeArea(self, ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> int:
        # s1+s2-overlap
        s1 = (ax2 - ax1) * (ay2 - ay1)
        s2 = (bx2 - bx1) * (by2 - by1)
        if ax1 > bx2 or bx1 > ax2 or ay1 > by2 or by1 > ay2: # 不重叠
            return s1 + s2
        # 想象合并区间
        # [  ]
        #   [   ]
        x = min(ax2, bx2) - max(ax1, bx1)
        y = min(ay2, by2) - max(ay1, by1)
        return s1 + s2 - x * y

# https://leetcode.cn/problems/circle-and-rectangle-overlapping/
# 矩形和圆形是否重叠
class Solution:
    def checkOverlap(self, radius: int, xCenter: int, yCenter: int, x1: int, y1: int, x2: int, y2: int) -> bool:
        # 圆心在内部
        if x1 <= xCenter <= x2 and y1 <= yCenter <= y2:
            return True
        # 圆心在上且相交
        if x1 <= xCenter <= x2 and y2 <= yCenter <= y2 + radius:
            return True
        # 圆心在下且相交
        if x1 <= xCenter <= x2 and y1 - radius <= yCenter <= y1:
            return True
        # 圆心在左且相交
        if x1 - radius <= xCenter <= x1 and y1 <= yCenter <= y2:
            return True
        # 圆心在右且相交
        if x2 <= xCenter <= x2 + radius and y1 <= yCenter <= y2:
            return True
        d = radius ** 2
        # 求圆心与顶点距离，小于等于r则相交
        for x in (x1, x2):
            for y in (y1, y2):
                if (xCenter - x) ** 2 + (yCenter - y) ** 2 <= d:
                    return True
        return False


# 曼哈顿距离转切比雪夫距离
# https://oi-wiki.org/geometry/distance/
# A(x1,y1), B(x2,y2)的曼哈顿距离 = |x1 - x2| + |y1 - y2|
# 等价于 (x1+y1, x1-y1), (x2+y2, x2-y2)两点的切比雪夫距离
# (x1',y1'),(x2',y2')的切比雪夫距离 = max(|x1' - x2'|, |y1' - y2'|)
# https://leetcode.cn/problems/minimize-manhattan-distances/
# 要求任意两点之间的最大曼哈顿距离，即求 max(max(x1-x2), max(y1-y2))
from sortedcontainers import SortedList
class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        xs = SortedList()
        ys = SortedList()
        for x, y in points:
            xs.add(x + y)
            ys.add(x - y)
        ans = inf
        for x, y in points:
            x, y = x + y, x - y
            xs.remove(x)
            ys.remove(y)
            ans = min(ans, max(xs[-1] - xs[0], ys[-1] - ys[0]))
            xs.add(x)
            ys.add(y)
        return ans
