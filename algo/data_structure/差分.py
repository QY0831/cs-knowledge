# 对数组a中连续子数组的操作，可以转变成对差分数组中两个数的操作
# 把 a[i],a[i+1] ... a[j] 加上 x
# 等价于将 d[i]+x, d[j+1]-x

# 初始化差分
n = len(nums)
d = [0] * (n + 1)
d[0] = nums[0]
for i in range(1, n):
    d[i] = nums[i] - nums[i-1]

# 差分数组还原原数组 (求前缀和)
arr = []
cur = 0
for x in d:
    cur += x
    arr.append(cur)
    

# 边修改差分数组边求前缀和
diff = [0] * n
sum_d = 0
for i, num in enumerate(nums):
    sum_d += diff[i]
    # 修改差分数组
    # 同时更新 diff 和 sum_d
    pass


# 拼车： https://leetcode.cn/problems/car-pooling/description/
class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        # trips[i]将from到to-1的数都增加numpass
        # 还原出原数组，并保证所有元素<=capacity
        # 也可以用Counter代替差分数组，只需更新from, to位置
        d = Counter()
        for num, from_, to in trips:
            d[from_] += num
            d[to] -= num
        # 还原差分，等价于key从小到大遍历，累加value
        s = 0
        for k in sorted(d):
            s += d[k]
            if s > capacity:
                return False
        return True

