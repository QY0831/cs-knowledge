# 线段树可以在 O(log N) 的时间复杂度内实现单点修改、区间修改、区间查询（区间求和，求区间最大值，求区间最小值）等操作。
# Atc template
import typing

class SegTree:
    def __init__(self,
                 op: typing.Callable[[typing.Any, typing.Any], typing.Any],
                 e: typing.Any,
                 v: typing.Union[int, typing.List[typing.Any]]) -> None:
        self._op = op # 线段树的合并操作，例如：max,add,gcd
        self._e = e # 线段树的值的幺元，默认大小(初始值)

        if isinstance(v, int): # 原数组（如果输入int则表示数组长度，用幺元生成数组）
            v = [e] * v

        self._n = len(v)
        self._log = self._ceil_pow2(self._n)
        self._size = 1 << self._log
        self._d = [e] * (2 * self._size)

        for i in range(self._n):
            self._d[self._size + i] = v[i]
        for i in range(self._size - 1, 0, -1):
            self._update(i)

    def _ceil_pow2(self, n: int) -> int:
        x = 0
        while (1 << x) < n:
            x += 1

        return x

    # 单点修改，修改a[p] = x，复杂度：o(logn)
    def set(self, p: int, x: typing.Any) -> None:
        assert 0 <= p < self._n

        p += self._size
        self._d[p] = x
        for i in range(1, self._log + 1):
            self._update(p >> i)

    # 单点查询，返回a[p]，复杂度：o(1)
    def get(self, p: int) -> typing.Any:
        assert 0 <= p < self._n

        return self._d[p + self._size]

    # 区间查询，返回op(a[l],……,a[r-1])，复杂度：o(logn)
    def prod(self, left: int, right: int) -> typing.Any:
        assert 0 <= left <= right <= self._n
        sml = self._e
        smr = self._e
        left += self._size
        right += self._size

        while left < right:
            if left & 1:
                sml = self._op(sml, self._d[left])
                left += 1
            if right & 1:
                right -= 1
                smr = self._op(self._d[right], smr)
            left >>= 1
            right >>= 1

        return self._op(sml, smr)

    # 返回op(a[0], ..., a[n - 1])，复杂度：o(1)
    def all_prod(self) -> typing.Any:
        return self._d[1]

    def _update(self, k: int) -> None:
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])


# https://leetcode.cn/problems/range-sum-query-mutable/
# 307. 区域和检索 - 数组可修改
class NumArray:

    def __init__(self, nums: List[int]):

        def op(p, q):
            return p + q

        self.t = SegTree(op, 0, nums)

    def update(self, index: int, val: int) -> None:
        self.t.set(index, val)

    def sumRange(self, left: int, right: int) -> int:
        return self.t.prod(left, right + 1)


# https://leetcode.cn/problems/peaks-in-array/
# 3187. 数组中的峰值
class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        # 单点修改：nums[idx] = val
        # 区间查询：nums中[l..r]中峰值元素的数目
        def op(a, b):
            return a + b
        n = len(nums)
        p = [0] * n # p[i]=1 是峰值；p[i]=0 不是峰值
        for i in range(1, n - 1):
            if nums[i - 1] < nums[i] and nums[i] > nums[i + 1]:
                p[i] = 1
        seg = SegTree(op, 0, p)

        ans = []
        for x, y, z in queries:
            if x == 1:
                if y + 1 >= z: # 区间长度至少为3
                    ans.append(0)
                else:
                    ans.append(seg.prod(y + 1, z)) # 按题意，头、尾不计入
            else:
                nums[y] = z
                for i in (y - 1, y, y + 1): # 更新受影响的3个位置是否为峰值
                    if 0 < i < n - 1:
                        if nums[i - 1] < nums[i] and nums[i] > nums[i + 1]:
                            seg.set(i, 1)
                        else:
                            seg.set(i, 0)
        return ans
