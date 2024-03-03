# 取出现频率最多的n个数
Counter(nums).most_common(n) # 返回值为 [(key1, value1) ... (keyn, valuen)]

# 遍历相邻元素
for p, q in pairwise(nums):
    pass

# 前缀和
# sum[i, j] = pre[j+1] - pre[i]
# sum[i, j) = pre[j] - pre[i] 左闭右开写法
pre = list(accumulate(arr, initial=0))

# 二分简洁写法
bisect_left(range(10**7+1), True, key=check)

# 组合两个数组并排序
s = sorted(zip(arr1, arr2))

# reduce：对数组中的元素连续操作
# reduce(function, iterable[, initializer])
# 先对集合中的第 1、2 个元素进行操作，得到的结果再与第三个数据用 function 函数运算...
sum = reduce(lambda x, y: x+y, [1,2,3,4,5]) # 15

# 取集合中最大或最小的n个, key可以定义比较内容
heapq.nlargest(n, iterable, key=None)
heapq.nsmallest(n, iterable, key=None)

# 弹出最小的值，并替换为新的值再加入堆 - 相当于heappop + heappush
heapreplace(nums, new_num)

# enumerate 定义下标从哪里开始
for idx, item in enumerate(arr, 1): # idx从1开始
    pass 

# SortedList
from sortedcontainers import SortedList
s = SortedList([])
s.add(1)
idx = s.index(1)  # 返回元素1的索引
s.remove(1) # 删除元素1
# 查找sortedlist中严格大于val的数量
# bisect_right方法返回的是将val插入到sortedlist中的索引位置。
# 由于sortedlist是有序的，所以这个索引位置之后的元素都严格大于val。
def helper(arr, val):
    return len(arr) - arr.bisect_right(val)
