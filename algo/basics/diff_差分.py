# 差分是一种和前缀和相对的策略，可以当做是求和的逆运算。
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


# https://leetcode.cn/problems/minimum-moves-to-make-array-complementary/description/
# 1674. 使数组互补的最少操作次数
# rating: 2333
class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        # res[x]: 和为x时，需要多少次操作
        # diff[x] = res[x] - res[x-1]
        # diff[0..x]的和表示res[x]
        # 遍历数对A, B，
        # 独立看每个数对，考虑A+B变成不同x，分别需要操作多少次
        # 对于范围在 [1 + min(A,B), limit + max(A,B)]的x -> 修改一次 -> diff[1+min(A,B)] + 1, diff[limit+max(A,B) + 1] -1
        # 对于范围在 [2, 2*limit] 范围的其他x -> 修改一次
        # 对于x=A+B -> 修改0次
        # 
        # 算法上可以先整体+2，再区间-1
        diff = [0] * (2 * limit + 2)
        n = len(nums)
        for i in range(n // 2):
            A, B = nums[i], nums[n - 1 - i]
            # add 2 on [2, 2*limit]
            diff[2] += 2
            diff[2 * limit + 1] -= 2

            # minus 1 on [1 + min(A,B), limit + max(A,B)]
            diff[1 + min(A,B)] -= 1
            diff[limit + max(A,B) + 1] += 1 

            # minus 1 on [A+B, A+B]
            diff[A + B] -= 1
            diff[A + B + 1] += 1

        res = n
        s = 0
        for i in range(2, 2 * limit + 1): # x范围[2, 2*limit]
            s += diff[i]
            if s < res:
                res = s
        return res


# https://leetcode.cn/problems/minimum-array-changes-to-make-differences-equal/description/
# 3224. 使差值相等的最少数组改动次数
class Solution:
    def minChanges(self, nums: List[int], k: int) -> int:
        # res[x] = sum(diff[0..x])
        # diff[x] = res[x] - res[x-1]
        # x范围[0, k]
        # 数对A,B, d = B - A (A < B)
        # 考虑d变成不同的x, 需要的操作次数
        # d最大能变成 max(k - A, B)，最小是0
        # 对于 x == d, 修改0次
        # 对于 x = [0, d - 1]，修改1次
        # 对于 x = [d + 1, max(k - A, B)], 修改1次
        # 对于 x = [max(k - A, B) + 1, k], 修改2次
        n = len(nums)
        diff = [0] * (k + 2)  # x范围[0, k], 差分数组长度k+1+1
        for i in range(n // 2):
            A, B = nums[i], nums[n - 1 - i]
            if A > B:
                A, B = B, A
            d = B - A
            mx = max(k - A, B)
            # add 1 [0, d - 1]
            diff[0] += 1
            diff[d] -= 1

            # add 1 [d + 1, mx]
            diff[d+1] += 1
            diff[mx+1] -= 1

            # add 2 [mx + 1, k]
            diff[mx+1] += 2
            # diff[k+1] -= 1

        return min(accumulate(diff)) 
