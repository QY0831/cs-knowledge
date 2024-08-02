# https://leetcode.cn/problems/possible-bipartition/description/
# 886. 可能的二分法
# rating: 1794
class Solution:
    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        g = defaultdict(list)
        color = [0] * n # 未染色

        def dfs(i, c):
            color[i] = c
            for j in g[i]:
                if color[j] == c:
                    return False
                if color[j] == 0 and not dfs(j, 3 - c): # 染另一种颜色
                    return False
            return True
        
        for a, b in dislikes:
            a -= 1
            b -= 1
            g[a].append(b)
            g[b].append(a)
        
        for i, c in enumerate(color):
            if c != 0:
                continue
            if not dfs(i, 1):
                return False
        return True
