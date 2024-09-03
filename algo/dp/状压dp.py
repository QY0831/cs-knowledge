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

