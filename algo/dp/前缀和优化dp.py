# https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-ii/description/
# 3251. 单调数组对的数目 II
class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        # n = len(nums)

        # 记忆化搜索
        # @cache
        # def f(i, pre1, pre2): # 枚举到i, arr1前一个数是pre1, arr2前一个数是pre2的方案数
        #     if i == n:
        #         return 1
        #     ans = 0
        #     for x in range(nums[i] + 1):
        #         y = nums[i] - x
        #         if x >= pre1 and y <= pre2:
        #             ans += f(i + 1, x, y)
        #     return ans
        
        # return f(0, -inf, inf) % 1_000_000_007

        # 递推
        # f[i][x] = sum(f[i - 1][lx] for lx in [0, x] if ly >= nums[i] - x)
        # n = len(nums)
        # mx = max(nums)
        # f = [[0 for _ in range(mx + 1)] for _ in range(n)]
        # for x in range(nums[0] + 1):
        #     f[0][x] = 1
        # for i in range(1, n):
        #     for x in range(nums[i] + 1):
        #         y = nums[i] - x
        #         for lx in range(min(x, nums[i-1]) + 1):
        #             ly = nums[i-1] - lx
        #             if ly >= y:
        #                 f[i][x] += f[i-1][lx]
        # return sum(f[-1]) % 1_000_000_007

        # 前缀和优化dp
        # f[i][x] = sum(f[i - 1][lx] for lx in [0, x] if ly >= nums[i] - x)
        # lx <= x
        # nums[i-1] - lx >= nums[i] - x
        # lx <= nums[i-1] - nums[i] + x
        # f[i][x] = sum(f[i-1][lx]), 
        # lx <= min(x, nums[i-1] - nums[i] + x)
        # lx <= x + min(0, nums[i-1] - nums[i])
        n = len(nums)
        mx = max(nums)
        f = [[0 for _ in range(mx + 1)] for _ in range(n)]
        for x in range(nums[0] + 1):
            f[0][x] = 1
        for i in range(1, n):
            s = list(accumulate(f[i-1]))
            for x in range(nums[i] + 1):
                lx = x + min(0, nums[i-1] - nums[i])
                f[i][x] += s[lx] % 1_000_000_007 if lx >= 0 else 0
                
        return sum(f[-1][:nums[-1]+1]) % 1_000_000_007
