from . import *

s = ascii_lowercase # "abcdef..." 得到所有字母
# https://docs.python.org/zh-tw/3.5/library/string.html
# 此模块中定义的常量为：

# string.ascii_letters
# 下文所述 ascii_lowercase 和 ascii_uppercase 常量的拼连。 该值不依赖于语言区域。

# string.ascii_lowercase
# 小写字母 'abcdefghijklmnopqrstuvwxyz'。 该值不依赖于语言区域，不会发生改变。

# string.ascii_uppercase
# 大写字母 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'。 该值不依赖于语言区域，不会发生改变。

# string.digits
# 字符串 '0123456789'。

# string.hexdigits
# 字符串 '0123456789abcdefABCDEF'。

# string.octdigits
# 字符串 '01234567'。

# string.punctuation
# 由在 C 语言区域中被视为标点符号的 ASCII 字符组成的字符串。

# string.printable
# 由被视为可打印符号的 ASCII 字符组成的字符串。 这是 digits, ascii_letters, punctuation 和 whitespace 的总和。

# string.whitespace
# 由被视为空白符号的 ASCII 字符组成的字符串。 其中包括空格、制表、换行、回车、进纸和纵向制表符。


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

# 堆化
heapify(h)

# 取集合中最大或最小的n个, key可以定义比较内容 （没有sort后切片快）
res = heapq.nlargest(n, iterable, key=None)
res = heapq.nsmallest(n, iterable, key=None)
mn, mn2 = heapq.nsmallest(2, iterable) # mn是最小值， mn2是次小值

# 弹出最小的值，并替换为新的值再加入堆 - 相当于heappop + heappush
heapq.heapreplace(nums, new_num)

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


# defaultdict 设置默认值
defaultdict(lambda: inf) # 默认value为inf


# 求所有组合
from itertools import combinations
res = combinations(nums,k) # nums中取k个的所有组合


from more_itertools import distinct_permutations
distinct_permutations(nums) # 返回所有不同的排列


# Python title() 方法返回"标题化"的字符串,就是说所有单词都是以大写开始，其余字母均为小写(见 istitle())。
str = "this is string example....wow!!!"
print(str.title()) # This Is String Example....Wow!!!


# 清理记忆化内存
@cache
def dfs():
    pass
dfs.cache_clear()


# filter
# filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。
a = filter(lambda x: x % 2 == 0, range(10)) # 过滤掉偶数


# The math.isqrt() method rounds a square root number downwards to the nearest integer.
# Examples to print the square root of different numbers
print(math.sqrt(10))  # 3.1622776601683795

# 开方并向下取整
# Round square root numbers downward to the nearest integer
print(math.isqrt(10)) # 3


# acm模式：读取输入
import sys
while True:
    s = input().split() # 一行一行读取
    a, b = int(s[0]), int(s[1])
    if not a and not b: # 遇到 0, 0 则中断
        break
    print(a + b)

