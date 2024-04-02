# low-bit: 得到最低位的1（2次幂）
while n:
    lb = n & -n
    n ^= lb


# 2的整数次幂满足
i & (i - 1) == 0


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
        ors = []  # 按位或的值，对应子数组的右端点的最小值
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
        n = len(arr)
        s = set()
        ans = inf
        for x in arr:
            s = {d & x for d in s}
            s.add(x)
            for d in s:
                ans = min(ans, abs(target - d))
        return ans