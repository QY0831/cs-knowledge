# low-bit: 得到最低位的1（2次幂）
while n:
    lb = n & -n
    n ^= lb


# 2的整数次幂满足
i & (i - 1) == 0


# 二进制枚举子集
nums = [1, 2, 3]
n = len(nums)
subsets = []
for mask in range(1, 1 << n):
    t = []
    for i in range(n):
        if mask & (1 << i): # nums[i]
            t.append(nums[i])
    subsets.append(t)


# 或值至少为k的最短子数组
# https://leetcode.cn/problems/shortest-subarray-with-or-at-least-k-ii/description/
class Solution:
    def minimumSubarrayLength(self, nums: List[int], k: int) -> int:
        # 定义dict保存
        # key: OR值 
        # value: 取得该OR值的最大左端点
        # 遍历右端点，更新字典，求当前右端点满足条件的最短子数组长度
        ans = inf
        d = dict()
        for i, x in enumerate(nums):
            d = {or_ | x: left for or_, left in d.items()} # update
            d[x] = i
            for or_, left in d.items():
                if or_ >= k:
                    ans = min(ans, i - left + 1)
        return ans if ans != inf else -1
    
    
# 按位或最大的最小子数组长度
# https://leetcode.cn/problems/smallest-subarrays-with-maximum-bitwise-or/description/
class Solution:
    def smallestSubarrays(self, nums: List[int]) -> List[int]:
        n = len(nums)
        d = dict()
        ans = [0] * n
        for i in range(n - 1, -1, -1):
            x = nums[i]
            # 更新 or_ 值对应的最近右边界
            d = {or_ | x : right for or_, right in d.items()}
            d[x] = i
            max_v = x
            ans[i] = 1
            for or_, right in d.items():
                if or_ > max_v:
                    ans[i] = right - i + 1
                    max_v = or_
        return ans
    
    
# 通用模板
# 1. 求出所有子数组的按位或的结果，以及值等于该结果的子数组的个数。
# 2. 求按位或结果等于任意给定数字的子数组的最短长度/最长长度。
class Solution:
    def smallestSubarrays(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [0] * n
        ors = []  # (按位或的值，对应子数组的右端点的最小值)
        for i in range(n - 1, -1, -1):
            num = nums[i]
            ors.append([0, i])
            k = 0
            for p in ors:
                p[0] |= num
                if ors[k][0] == p[0]:
                    ors[k][1] = p[1]  # 合并相同值，下标取最小的
                else:
                    k += 1
                    ors[k] = p
            del ors[k + 1:]
            # 本题只用到了 ors[0]，如果题目改成任意给定数值，可以在 ors 中查找
            ans[i] = ors[0][1] - i + 1
        return ans


# 找到所有可能的子数组的与运算的合
# https://leetcode.cn/problems/find-a-value-of-a-mysterious-function-closest-to-target/
class Solution:
    def closestToTarget(self, arr: List[int], target: int) -> int:
        s = set()
        ans = inf
        for x in arr:
            s = {d & x for d in s}
            s.add(x)
            for d in s:
                ans = min(ans, abs(target - d))
        return ans
    

# logTrick: 
# https://github.com/981377660LMT/algorithm-study/blob/0f29c59a3d7fb8c56ea21fa54b6ed8b5682e34c9/21_%E4%BD%8D%E8%BF%90%E7%AE%97/logTrick/logTrick.py#L7
def logTrick(
    nums: List[int],
    op: Callable[[int, int], int],
    f: Optional[Callable[[List[Tuple[int, int, int]], int], None]] = None,
) -> DefaultDict[int, int]:
    """
    将 `nums` 的所有非空子数组的元素进行 `op` 操作，返回所有不同的结果和其出现次数.

    Args:
        nums: 1 <= len(nums) <= 1e5.
        op: 与/或/gcd/lcm 中的一种操作，具有单调性.
    
        定义f对当前下标为止的结果进行处理：(optional)
        f: (interval: List[Tuple[int, int, int]], right: int) -> None
        interval: [leftStart, leftEnd, value]
        数组的右端点为right.
        interval 的 leftStart/leftEnd 表示子数组的左端点left的范围.
        interval 的 value 表示该子数组 arr[left,right] 的 op 结果.

    Returns:
        所有不同的结果和其出现次数
    """
    res = defaultdict(int)
    dp = []
    for pos, cur in enumerate(nums):
        for v in dp:
            v[2] = op(v[2], cur) # 更新value
        dp.append([pos, pos + 1, cur]) # 新增interval [pos, pos + 1, cur]，只包含当前元素

        ptr = 0
        for v in dp[1:]: 
            if dp[ptr][2] != v[2]: # op结果不同，
                ptr += 1
                dp[ptr] = v
            else:
                dp[ptr][1] = v[1]
        dp = dp[: ptr + 1]

        for v in dp:
            res[v[2]] += v[1] - v[0]
            
        if f is not None:
            f(dp, pos)

    return res

# 简化版本：
def logTrick(nums, op):
    res = defaultdict(int)
    dp = []
    for pos, cur in enumerate(nums):
        for v in dp:
            v[2] = op(v[2], cur)
        dp.append([pos, pos + 1, cur])

        ptr = 0
        for v in dp[1:]: 
            if dp[ptr][2] != v[2]: 
                ptr += 1
                dp[ptr] = v
            else:
                dp[ptr][1] = v[1]
        dp = dp[: ptr + 1]

        for v in dp:
            res[v[2]] += v[1] - v[0]
    return res
    
    
if __name__ == "__main__":
    from operator import and_, or_
    from math import gcd, lcm

    # 1521. 找到最接近目标值的函数值
    class Solution2:
        def closestToTarget(self, arr: List[int], target: int) -> int:
            counter = logTrick(arr, lambda x, y: x & y)
            return min(abs(k - target) for k in counter)

    # 2941. 子数组的最大 GCD-Sum
    # https://leetcode.cn/problems/maximum-gcd-sum-of-a-subarray/description/
    class Solution:
        def maxGcdSum(self, nums: List[int], k: int) -> int:
            def f(interval: List[Tuple[int, int, int]], right: int) -> None:
                nonlocal res
                for start, _, gcd_ in interval:
                    len_ = right - start + 1
                    if len_ >= k:
                        res = max(res, gcd_ * (preSum[right + 1] - preSum[start]))

            res = 0
            preSum = list(accumulate(nums, initial=0))
            logTrick(nums, gcd, f)
            return res

