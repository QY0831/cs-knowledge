# https://leetcode.cn/problems/number-of-ways-to-wear-different-hats-to-each-other/description/
# 1434. 每个人戴不同帽子的方案数
# rating: 2273
class Solution:
    def numberWays(self, hats: List[List[int]]) -> int:
        mp = [[] for _ in range(41)]
        mx = 1
        for i, h in enumerate(hats):
            for x in h:
                mp[x].append(i)
                if x > mx:
                    mx = x
        
        a = (1 << len(hats)) - 1

        @cache
        def f(i, j): # i:帽子 j:已选帽子的人
            if i == 0:
                return 1 if j == a else 0 # 所有人都戴了帽子
            
            res = f(i - 1, j) # 跳过i

            for k in mp[i]:
                if j & (1 << k) == 0: # k还没选帽子
                    res += f(i - 1, j | (1 << k)) # 给k戴帽子i
            return res % 1_000_000_007

        return f(mx, 0)


# https://leetcode.cn/problems/maximum-number-of-moves-to-kill-all-pawns/description/
# 3283. 吃掉所有兵需要的最多移动次数
# bfs+状态压缩+博弈论
class Solution:
    def maxMoves(self, kx: int, ky: int, positions: List[List[int]]) -> int:
        # 预处理：dis[i][x][y]=第i个小兵被(x,y)吃掉的最小步数
        # mask: 没吃掉的兵为0
        # i: 马在第i个兵的位置 (x, y)
        # 枚举吃第j个兵，若j没被吃掉，则
        # alice:  f(i, mask) = Ej-Max f(j, mask OR {j}) + dis[j][x][y] 
        # bob:    f(i, mask) = Ej-Min f(j, mask OR {j}) + dis[j][x][y] 
        n = len(positions)
        dis = [[[-1] * 50 for _ in range(50)] for _ in range(n)]
        dirs = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))

        for d, (px, py) in zip(dis, positions):
            d[px][py] = 0
            q = deque([(px, py)])
            step = 1
            while q:
                size = len(q)
                for _ in range(size):
                    x, y = q.popleft()
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 50 and 0 <= ny < 50 and d[nx][ny] < 0:
                            d[nx][ny] = step
                            q.append((nx, ny))
                step += 1
        
        done = (1 << (n + 1)) - 1
        positions.append([kx, ky])
        init = 1 << n

        @cache
        def dfs(i, mask, alice):
            if mask == done:
                return 0
            x, y = positions[i]
            if alice:
                res = 0
                for j, d in enumerate(dis):
                    if mask & (1 << j) == 0:
                        res = max(res, dfs(j, mask | (1 << j), False) + d[x][y])
            else:
                res = inf
                for j, d in enumerate(dis):
                    if mask & (1 << j) == 0:
                        res = min(res, dfs(j, mask | (1 << j), True)+ d[x][y])
            return res


        return dfs(n, init, True)


# https://leetcode.cn/problems/maximum-and-sum-of-array/
# 2172. 数组的最大与和
# rating: 2392
# 三进制状态压缩
class Solution:
    def maximumANDSum(self, nums: List[int], numSlots: int) -> int:
        n = len(nums)

        @cache
        def f(i, slot_mask1, slot_mask2):
            if i == n:
                return 0

            def _in(idx, ma):
                return (ma & (1 << idx)) > 0
            
            def _add(idx, ma):
                return ma | (1 << idx)
            
            res = 0
            for s in range(numSlots):
                if not _in(s, slot_mask1):
                    res = max(
                        res,
                        ((s + 1) & nums[i]) + f(i + 1, _add(s, slot_mask1), slot_mask2)
                    )
                elif not _in(s, slot_mask2):
                    res = max(
                        res,
                        ((s + 1) & nums[i]) + f(i + 1, slot_mask1, _add(s, slot_mask2))
                    )
            return res

        return f(0, 0, 0)
