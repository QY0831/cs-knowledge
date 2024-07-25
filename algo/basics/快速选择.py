# https://leetcode.cn/problems/kth-largest-element-in-an-array/
# O(n)快速选择数组种第k个最大元素
def quickselect(nums, l, r, k):
    if l == r:
        return nums[k]
    partition = nums[l]
    i, j = l - 1, r + 1
    while i < j:
        i += 1
        while nums[i] < partition:
            i += 1
        j -= 1
        while nums[j] > partition:
            j -= 1
        if i < j:
            nums[i], nums[j] = nums[j], nums[i]
    if k <= j:
        return quickselect(nums, l, j, k)
    else:
        return quickselect(nums, j + 1, r, k)

def findKthLargest(nums, k):
    n = len(nums)
    return quickselect(nums, 0, n - 1, n - k)