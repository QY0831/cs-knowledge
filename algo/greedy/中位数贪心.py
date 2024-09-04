# pos = [0,1,5]
# 在坐标轴上的 0,1,5 位置上有 3 个生产商品的工厂，我们要建造一个货仓存放商品，把货仓建在哪里，可以使所有工厂到货仓的距离之和最小？
# 这个问题叫做「货仓选址」。根据 中位数贪心及其证明，最优解是把货仓建在工厂位置的中位数上。
# 设cost[i][j]表示在工厂i和工厂j之间建一个货仓的最小距离和，
# 那么cost[i][j] = cost[i+1][j-1] + pos[j] - pos[i]， 可以预处理出cost数组（例题：1478. 安排邮筒）


# https://leetcode.cn/problems/minimum-operations-to-make-all-array-elements-equal/description/
# rating: 1903
# 2602. 使数组元素全部相等的最少操作次数
# 利用前缀和，可以O(1)时间内求出子数组元素到其中位数的距离之和
class Solution:
    def minOperations(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)
        nums.sort()
        s = list(accumulate(nums, initial=0)) # 1,2,3 -> 0,1,3,6 
        ans = []
        for q in queries:
            j = bisect_left(nums, q) # nums[j:] >= q
            left = q * j - s[j] # 共j个数<q, s[j]为前j个数的前缀和
            right = s[n] - s[j] - q * (n - j)
            ans.append(left + right)
        return ans


# https://leetcode.cn/problems/minimum-moves-to-pick-k-ones/description/
# rating: 2672
# 3086. 拾起 K 个 1 需要的最少行动次数
class Solution:
    def minimumMoves(self, nums: List[int], k: int, maxChanges: int) -> int:
        # 目标： 使用最少数量的行动次数从 nums 中拾起 k 个 1
        # 初始： 选择一个index，若nums[index]==1，则拾取变更新nums[index]=0
        # 执行操作：
        #   1. 设置任意nums[j]=0的j位置（除当前位置外）变成1，最多操作maxChanges次
        #   2. 选择任意两个相邻的值不相等下标i,j，交换值，若值为0的位置是当前位置，则拾取一个k
        #
        #  操作2:若想得到一个位置在j的1，则需要交换 |alice - j| 次
        #  操作1:把alice相邻的0变成1，再执行操作2，即可通过两次操作得到1
        # 
        # 贪心：尽可能选择111的中间位置作为起始，则可通过2次操作得到2个1，其次选择11，则可通过1次操作得到1个1， 其次选择1开始。。。
        # 1. 假设有连续的c个1，（若c > k, 则取c=k）
        #  那么可以通过c-1次操作得到c-1个1，剩余k-c个1，使用2次操作得到, 共c-1 + 2*(k-c)次，
        #  前提是 maxChanges >= k - c
        # 2. 若 maxChanges = 0， 即只能通过交换来得到1
        #  即【中位数贪心】，在数组中找一个位置，到所有1的距离之和最小，应把位置选在所有1位置的中位数上
        # 3. 0 < maxChanges < k - c
        #  先求所有长为 k - maxChanges 的子数组的【中位数贪心】，取最小值；再通过2 * maxChanges得到剩余的1
        # 情况2、3可以合并处理
        pos = []
        c = 0
        cnt = 0
        for i, x in enumerate(nums):
            if x == 0:
                cnt = 0
                continue
            pos.append(i)
            cnt += 1
            c = max(cnt, c)
        if c > 3:
            c = 3
        if c > k:
            c = k
        if maxChanges >= k - c:
            return max(c - 1, 0) + 2 * (k - c)
        
        n = len(pos)
        pre = list(accumulate(pos, initial=0))
        ans = inf
        size = k - maxChanges
        for right in range(size, n + 1): # 遍历长为 k - maxChanges的子数组
            left = right - size
            # 中位数
            i = left + size // 2
            # s1: pos[i]与pos[left..i]的距离之和
            s1 = pos[i] * (i - left) - (pre[i] - pre[left])
            # s2: pos[i]与pos[i..right]的距离之和
            s2 = pre[right] - pre[i] - pos[i] * (right - i)
            ans = min(ans, s1 + s2)
        return ans + maxChanges * 2


# https://leetcode.cn/problems/allocate-mailboxes/
# 1478. 安排邮筒
# rating: 2190
class Solution:
    def minDistance(self, houses: List[int], k: int) -> int:
        # cost[i][j]: 在house[i],house[j]间放一个邮筒的最小总花费，放在中位数处总和最小
        # 1 4 8 9 20
        # med = 8
        # 4 8 9
        # med = 8
        # cost[i][j] = cost[i+1][j-1] + house[j] - house[i]
        n = len(houses)
        houses.sort()
        cost = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n): # j > i
                if i == j:
                    cost[i][j] = 0
                else:
                    cost[i][j] = cost[i+1][j-1] + houses[j] - houses[i]
        
        # f[i][j]: 前i个房子，放j个邮筒的最小距离和
        # f[i][j] = min(f[L][j-1] + cost[L][i], L:[0,i-1], j:[2, min(i+1, k)])
        f = [[inf] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 0
        for i in range(1, n + 1):
            f[i][1] = cost[0][i - 1]
            for j in range(2, min(i+1, k) + 1):
                for L in range(i):
                    if f[L][j-1] != inf:
                        f[i][j] = min(f[i][j], f[L][j-1] + cost[L][i-1])
        return f[-1][-1]
