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
