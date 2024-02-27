def check(x) -> bool:
    pass

# 返回满足条件的最左下标(前提是一定有解，否则还需要检查最后left位置的数)
def bsearch_left(left, right):
    while left < right:
        mid = (left + right) // 2
        if not check(mid):
            left = mid + 1
        else:
            right = mid
    return left

# 返回满足条件的最右下标(前提是一定有解，否则还需要检查最后left位置的数)
def bsearch_right(left, right):
    while left < right:
        mid = (left + right + 1) // 2
        if not check(mid):
            right = mid - 1
        else:
            left = mid
    return left

# 库函数
bisect_left(arr, True, key=check) # arr中满足check的最小下标
