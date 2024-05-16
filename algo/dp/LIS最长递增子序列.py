# LIS
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        t = [] # t[i] 长度为i+1的序列的末尾最小值
        for x in nums:
            j = bisect_left(t, x) # 非严格递增改成 bisect_right
            if j == len(t):
                t.append(x)
            else:
                t[j] = x
        return len(t)


# 最长递增子序列方案数
class Solution:
    def findNumberOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        max_len = 1
        ans = 1
        f = [1] * n
        cnt = [1] * n
        for i in range(1, n):
            for j in range(i):
                if nums[i] > nums[j]:
                    if f[j] + 1 > f[i]:
                        f[i] = f[j] + 1
                        cnt[i] = cnt[j]
                    elif f[j] + 1 == f[i]:
                        cnt[i] += cnt[j]
            if f[i] > max_len:
                max_len = f[i]
                ans = cnt[i]
            elif f[i] == max_len:
                ans += cnt[i]
        return ans
