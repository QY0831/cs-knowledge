# https://oi-wiki.org/graph/mst/
# 我们定义无向连通图的 最小生成树（Minimum Spanning Tree，MST）为边权和最小的生成树。

# Kruskal 算法是一种常见并且好写的最小生成树算法，由 Kruskal 发明。该算法的基本思想是从小到大加入边，是个贪心算法。
# 为了造出一棵最小生成树，我们从最小边权的边开始，按边权从小到大依次加入，如果某次加边产生了环，就扔掉这条边，
# 直到加入了 n-1 条边，即形成了一棵树。
# Kruskal 算法的时间复杂度为 O(mlogm)，其中 m 是边数。

class UnionFind:
    def __init__(self, n, size=None):
        self.parent = list(range(n))
        self.size = [1] * n if size is None else size
        self.part = n # 连通分量

    def find(self, a):
        if self.parent[a] != a:
            self.parent[a] = self.find(self.parent[a])
        return self.parent[a]

    def merge(self, a, b):
        pa, pb = self.find(a), self.find(b)
        if pa == pb: 
            return False
        if self.size[pa] < self.size[pb]:
            self.parent[pa] = pb
            self.size[pb] += self.size[pa]
        else:
            self.parent[pb] = pa
            self.size[pa] += self.size[pb]
        self.part -= 1
        return True

    def get_size(self, a):
        return self.size[self.find(a)]

# https://leetcode.cn/problems/min-cost-to-connect-all-points/
class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                edges.append((dist, i, j))
        edges.sort() # 按边权排序
        uf = UnionFind(n)
        ans = 0
        cnt = 0 # 边数
        for d, a, b in edges: # 从小到大加入边
            if uf.merge(a, b): 
                ans += d
                cnt += 1
                if cnt == n - 1: # 直到边数为 n - 1
                    break
        return ans