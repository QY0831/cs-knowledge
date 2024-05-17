# 线段树可以在 O(log N) 的时间复杂度内实现单点修改、区间修改、区间查询（区间求和，求区间最大值，求区间最小值）等操作。

class SegmentTree:
    
    def __init__(self, n: int) -> None:
        self.sum = [0] * (4 * n)
        
    def add(self, o: int, l: int, r: int, idx: int, val: int): 
        # o: 当前节点的编号
        # 左子树编号: 2 * o
        # 右子树编号: 2 * o + 1
        # l, r: 当前节点对应的区间
        if l == r:
            self.sum[l] += val
            return
        mid = (l + r) // 2
        if idx <= mid:
            self.add(o * 2, l, mid, idx, val)
        else:
            self.add(o * 2 + 1, mid + 1, r, idx, val)
        self.sum[o] = self.sum[o * 2] + self.sum[o * 2 + 1]
    
    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        # L, R: 查询区间
        if L <= l and r <= R:
            return self.sum[o] # o被完全包含在[L, R]中
        sum_ = 0
        mid = (l + r) // 2
        if L <= mid:
            sum_ += self.query(o * 2, l, mid, L, R)
        if R > mid:
            sum_ += self.query(o * 2 + 1, mid + 1, r, L, R)
        return sum_


# 线段树求最长递增子序列
# https://leetcode.cn/problems/longest-increasing-subsequence-ii/description/
# 利用线段树维护以j结尾的最大子序列长度(求区间最大值)
class Solution:

    def __init__(self):
        self.mx = None

    def update(self, o: int, l: int, r: int, idx: int, val: int): 
        if l == r:
            self.mx[o] = val
            return
        mid = (l + r) // 2
        if idx <= mid:
            self.update(o * 2, l, mid, idx, val)
        else:
            self.update(o * 2 + 1, mid + 1, r, idx, val)
        self.mx[o] = max(self.mx[o * 2], self.mx[o * 2 + 1])

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.mx[o]
        res = 0
        mid = (l + r) // 2
        if L <= mid:
            res = self.query(o * 2, l, mid, L, R)
        if R > mid:
            res = max(res, self.query(o * 2 + 1, mid + 1, r, L, R))
        return res

    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        # f[i][j] = max(f[i-1][j']) + 1
        # j - k <= j' < j
        u = max(nums) # 数组范围[1,u], n = u, 线段树size=n * 4
        self.mx = [0] * (4 * u) # 保存j对应的最大子序列长度
        for x in nums:
            if x == 1:
                self.update(1, 1, u, 1, 1) # 以1为结尾的最大子序列长度必为1
            else:
                res = 1 + self.query(1, 1, u, max(x - k, 1), x - 1) # 查询区间内最大长度
                self.update(1, 1, u, x, res) # 更新j=x对应的最大值
        return self.mx[1] # 根节点对应整个数组对应的最大长度
