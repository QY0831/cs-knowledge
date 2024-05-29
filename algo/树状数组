# SortedList
# api: https://grantjenks.com/docs/sortedcontainers/sortedlist.html
from sortedcontainers import SortedList
sl = SortedList([])
sl.add(1)
i = s.index(1)  # 返回第一个元素1的索引
s.remove(1) # 删除元素1, 1必须存在
s.discard(1) # 删除元素1，1可以不存在
i = sl.bisect_left(1) # 插入1的位置, sl[i] >= 1
j = sl.bisect_left(1) # 插入1的最右位置, j = len(sl) or sl[j] > 1

small_cnt = sl.bisect_left(val) # 查找sortedlist中严格小于val的数量
large_cnt = len(sl) - sl.bisect_right(val) # 查找sortedlist中严格大于val的数量