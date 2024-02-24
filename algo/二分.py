def check(x):
    pass

# 返回满足条件的最左下标
def bsearch_left(left, right):
    while left < right:
        mid = (left + right) // 2
        if not check(mid):
            left = mid + 1
        else:
            right = mid
    return left

# 返回满足条件的最右下标
def bsearch_right(left, right):
    while left < right:
        mid = (left + right + 1) // 2
        if not check(mid):
            right = mid - 1
        else:
            left = mid
    return left


