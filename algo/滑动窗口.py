# 定长滑动窗口
# https://leetcode.cn/problems/number-of-unique-flavors-after-sharing-k-candies/description/
# 2107. 分享 K 个糖果后独特口味的数量
class Solution:
    def shareCandies(self, candies: List[int], k: int) -> int:
        if k == 0:
            return len(set(candies))
        ans = 0
        tot = Counter(candies)
        for i, x in enumerate(candies):
            tot[x] -= 1  # 入窗
            if tot[x] == 0:
                del tot[x]
                
            if i < k - 1:
                continue
            
            if len(tot) > ans: # 更新答案
                ans = len(tot)

            pre = candies[i - k + 1] # 出窗
            tot[pre] += 1
        return ans


# 不定长滑动窗口
# 主要分为三类：求最长子数组，求最短子数组，以及求子数组个数。
# https://leetcode.cn/problems/minimum-operations-to-reduce-x-to-zero/
class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        left = cur = 0
        ans = -1
        s = sum(nums)
        t = s - x
        if t < 0:
            return -1
        for i, d in enumerate(nums): # 求和为t的最长子数组
            cur += d
            while cur > t:
                cur -= nums[left]
                left += 1
            if cur == t:
                ans = max(ans, i - left + 1)
        if ans == -1:
            return -1
        return len(nums) - ans 


# https://leetcode.cn/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/description/
# 滑动窗口最大最小值
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


# SlidingWindowAggregation 是一个维护幺半群的滑动窗口的数据结构
# 可以在 O(1) 时间内做到入队、出队、查询滑窗内的聚合值

from typing import Callable, Generic, List, TypeVar

E = TypeVar("E")

class SlidingWindowAggregation(Generic[E]):
    """SlidingWindowAggregation

    Api:
    1. append value to tail,O(1).
    2. pop value from head,O(1).
    3. query aggregated value in window,O(1).
    """

    __slots__ = ["_stack0", "_stack1", "_stack2", "_stack3", "_e0", "_e1", "_size", "_op", "_e"]

    def __init__(self, e: Callable[[], E], op: Callable[[E, E], E]):
        """
        Args:
            e: unit element
            op: merge function
        """
        self._stack0 = []
        self._stack1 = []
        self._stack2 = []
        self._stack3 = []
        self._e = e
        self._e0 = e()
        self._e1 = e()
        self._size = 0
        self._op = op

    def append(self, value: E) -> None:
        if not self._stack0:
            self._push0(value)
            self._transfer()
        else:
            self._push1(value)
        self._size += 1

    def popleft(self) -> None:
        if not self._size:
            return
        if not self._stack0:
            self._transfer()
        self._stack0.pop()
        self._stack2.pop()
        self._e0 = self._stack2[-1] if self._stack2 else self._e()
        self._size -= 1

    def query(self) -> E:
        return self._op(self._e0, self._e1)

    def _push0(self, value):
        self._stack0.append(value)
        self._e0 = self._op(value, self._e0)
        self._stack2.append(self._e0)

    def _push1(self, value):
        self._stack1.append(value)
        self._e1 = self._op(self._e1, value)
        self._stack3.append(self._e1)

    def _transfer(self):
        while self._stack1:
            self._push0(self._stack1.pop())
        while self._stack3:
            self._stack3.pop()
        self._e1 = self._e()

    def __len__(self):
        return self._size


# 例子：
# 求gcd为1的最短子数组
INF = int(1e20)

class Solution:
    def minOperations(self, nums: List[int]) -> int:
        if gcd(*nums) != 1:
            return -1
        if 1 in nums:
            return len(nums) - nums.count(1)
        return minLen(nums) - 1 + len(nums) - 1


def minLen(nums: List[int]) -> int:
    """gcd为1的最短子数组.不存在返回INF."""
    n = len(nums)
    S = SlidingWindowAggregation(lambda: 0, gcd)
    res, n = INF, len(nums)
    for right in range(n):
        S.append(nums[right])
        while S and S.query() == 1:
            res = min(res, len(S))
            S.popleft()
    return res



# 两次滑动窗口求恰好包含k个辅音的子字符串数
# https://leetcode.cn/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/
class Solution:

    def f(self, word, k): # 每个元音字母至少出现一次，并且至少包含 k 个辅音字母的子字符串的总数
        vowels = 'aeiou'
        cnt1 = defaultdict(int)
        cnt2 = 0
        ans = 0
        left = 0
        ans = 0
        for c in word:
            if c in vowels:
                cnt1[c] += 1
            else:
                cnt2 += 1
            while len(cnt1) == 5 and cnt2 >= k: # 压缩左边界直到不符合
                x = word[left]
                if x in vowels:
                    cnt1[x] -= 1
                    if cnt1[x] == 0:
                        del cnt1[x]
                else:
                    cnt2 -= 1
                left += 1
            ans += left # 此时右边界right,左边界<left的子串，都符合条件
        return ans

    def countOfSubstrings(self, word: str, k: int) -> int:
        # 恰好k个=至少包含k个辅音字符-至少包含k+1个辅音字符
        return self.f(word, k) - self.f(word, k+1)
