from bisect import *

def check(x) -> bool:
    pass

# 返回满足条件的最左下标(前提是一定有解，否则还需要检查最后left位置的数)
def bsearch_left(left, right):
    while left < right:
        mid = (left + right) // 2
        if not check(mid): # 不满足条件时，需要增大
            left = mid + 1
        else:
            right = mid
    return left

# 返回满足条件的最大值(前提是一定有解，否则还需要检查最后left位置的数)
def bsearch_valid_max(left, right):
    while left < right:
        mid = (left + right + 1) // 2
        if not check(mid): # 不满足条件时，需要减小
            right = mid - 1
        else:
            left = mid
    return left

# 库函数
bisect_left(arr, True, key=check) # arr中满足check的最小下标
# 这两个函数的返回值可以被视为表示插入点的索引
sequence = [1, 2, 2, 3, 4, 4, 6, 8, 9, 10]
left_index = bisect_left(sequence, 4)
right_index = bisect_right(sequence, 4)
print(left_index)   # 输出为 4
print(right_index)  # 输出为 6

# 查找sortedlist中严格大于val的数量
def helper(arr, val):
    return len(arr) - arr.bisect_right(val)

# 二分查找[low, high]范围内的数的个数
bisect_right(nums, high) - bisect_left(nums, low) 
