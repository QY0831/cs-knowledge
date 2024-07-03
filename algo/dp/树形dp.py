# 树的直径：树的直径是树中最长路径的长度。树的直径等于树中任意两点之间的最长路径的长度。
def diameter(edges: List[List[int]], ) -> int:
    g = [[] for _ in range(len(edges) + 1)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)

    res = 0
    def dfs(x: int, fa: int) -> int:
        nonlocal res
        max_len = 0
        for y in g[x]:
            if y != fa:
                sub_len = dfs(y, x) + 1
                res = max(res, max_len + sub_len)
                max_len = max(max_len, sub_len)
        return max_len
    dfs(0, -1)
    return res


def diameterOfBinaryTree(root: Optional[TreeNode]) -> int:
    res = 0
    def dfs(x):
        if not x:
            return 0
        nonlocal res
        left = dfs(x.left)
        right = dfs(x.right)
        res = max(res, left + right + 1)
        return max(left, right) + 1
    
    dfs(root)
    return res - 1


# https://leetcode.cn/problems/longest-path-with-different-adjacent-characters/description/
# 找出路径上任意一对相邻节点都没有分配到相同字符的 最长路径 
class Solution:
    def longestPath(self, parent: List[int], s: str) -> int:
        n = len(parent)
        graph = [[] for _ in range(n)]
        for i, p in enumerate(parent):
            if p != -1:
                graph[p].append(i)
        ans = 0

        def dfs(x):
            nonlocal ans
            max_len = 0  # 从x出发的最长路径
            for y in graph[x]:
                _len = dfs(y) + 1  # 从x-y出发的最长路径, 这行必须跑，否则y不会被查询
                if s[x] != s[y]:  # 该路径有效
                    ans = max(ans, max_len + _len)  # 更新答案
                    max_len = max(max_len, _len)  # 更新最长路径
            return max_len

        dfs(0)
        return ans + 1


# https://leetcode.cn/problems/find-minimum-diameter-after-merging-two-trees/description/
# 合并两棵树后的最小直径
# 经典结论：两棵树合并后，新直径的两个端点，一定是原来两棵树直径的四个端点里的其中两个。
# 如果新直径不经过合并边，那么它就是原来两个直径中的较大值。
# 如果新直径经过合并边，则新直径的端点一定是原来两个直径的端点。
# max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)
class Solution:
    def diameter(self, edges: List[List[int]], ) -> int:
        g = [[] for _ in range(len(edges) + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        res = 0
        def dfs(x: int, fa: int) -> int:
            nonlocal res
            max_len = 0
            for y in g[x]:
                if y != fa:
                    sub_len = dfs(y, x) + 1
                    res = max(res, max_len + sub_len)
                    max_len = max(max_len, sub_len)
            return max_len
        dfs(0, -1)
        return res

    def minimumDiameterAfterMerge(self, edges1: List[List[int]], edges2: List[List[int]]) -> int:
        d1 = self.diameter(edges1)
        d2 = self.diameter(edges2)
        return max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)


#https://leetcode.cn/problems/count-subtrees-with-max-distance-between-cities/description/
#1617. 统计子树中城市之间最大距离
class Solution:
    def countSubgraphsForEachDiameter(self, n: int, edges: List[List[int]]) -> List[int]:
        # 1.遍历所有子树（每棵树选或不选两种状态），n个树，共 1<<n种状态
        # 2.求每种状态下，有且仅有一个子树下 - 树的直径
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a - 1].append(b - 1)
            g[b - 1].append(a - 1)
        
        ans = [0] * (n - 1)
        select = [False] * n

        def f(i):
            if i == n: # 计算当前状态
                vis = [False] * n  # 记录访问过的节点
                res = 0 # 直径
                def dfs(x: int, fa: int) -> int:
                    nonlocal res
                    max_len = 0
                    vis[x] = True
                    for y in g[x]:
                        if y != fa and select[y]:
                            sub_len = dfs(y, x) + 1
                            res = max(res, max_len + sub_len)
                            max_len = max(max_len, sub_len)
                    return max_len
                for i in range(n):
                    if not select[i]:
                        continue
                    # 随便选一个作为起点，计算直径
                    dfs(i, -1)
                    break
                if res and vis == select: # 有且仅有一个子树
                    ans[res - 1] += 1
                return 
            
            f(i + 1)

            select[i] = True
            f(i + 1)
            select[i] = False
        
        f(0)
        return ans
