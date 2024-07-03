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


# 合并两棵树后的最小直径
# 经典结论：两棵树合并后，新直径的两个端点，一定是原来两棵树直径的四个端点里的其中两个。
# 如果新直径不经过合并边，那么它就是原来两个直径中的较大值。
# 如果新直径经过合并边，则新直径的端点一定是原来两个直径的端点。
# max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)
# https://leetcode.cn/problems/find-minimum-diameter-after-merging-two-trees/description/
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

