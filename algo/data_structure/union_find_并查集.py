class UnionFind:
    """并查集维护无向图每个连通块的边数和顶点数"""
    def __init__(self, n, size=None):
        self.n = n
        self.parent = list(range(n))
        self.size = [1] * n if size is None else size # 每个联通块的顶点数
        self.part = n # 连通分量
        self.edge = [0] * n  # 每个联通块的边数

    def find(self, a):
        if self.parent[a] != a:
            self.parent[a] = self.find(self.parent[a])
        return self.parent[a]

    def merge(self, a, b):
        pa, pb = self.find(a), self.find(b)
        if pa == pb: 
            self.edge[pa] += 1
            return False
        if self.size[pa] < self.size[pb]:
            pa, pb = pb, pa

        self.parent[pb] = pa
        self.size[pa] += self.size[pb]
        self.edge[pa] += self.edge[pb] + 1
        self.part -= 1
        return True

    def is_connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def get_size(self, a):
        return self.size[self.find(a)]
    
    def get_groups(self): # 返回每个连通块的元素
        groups = defaultdict(list)
        for key in range(self.n):
            root = self.find(key)
            groups[root].append(key)
        return groups

    def get_roots(self): # 返回所有根节点
        return list(set(self.find(i) for i in range(self.n)))

    def __repr__(self) -> str:
        return "\n".join(f"{root}: {member}" for root, member in self.getGroups().items())

    def __len__(self) -> int:
        return self.part
    
    

# https://leetcode.cn/problems/count-the-number-of-complete-components/description/
# 2685. 统计完全连通分量的数量
# 难度：1769
class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        uf = UnionFind(n)
        path = []
        for a, b in edges:
            uf.merge(a, b)
            path.append(a)
        
        ans = 0
        for v in uf.get_roots():
            if comb(uf.size[v], 2) == uf.edge[v]:
                ans += 1
        return ans

    
# https://leetcode.cn/problems/find-latest-group-of-size-m/
# 1562. 查找大小为 M 的最新分组
# 难度: 1928
# 利用并查集合并区间
class Solution:
    def findLatestStep(self, arr: List[int], m: int) -> int:
        n = len(arr)
        uf = UnionFind(n + 1) # 将size初始化为0
        ans = -1
        cnt = [0] *  (n + 1)
        
        for i, p in enumerate(arr):
            uf.size[p] = 1
            cnt[1] += 1 
            if p > 1 and uf.size[uf.find(p - 1)] > 0:
                cnt[uf.size[uf.find(p - 1)]] -= 1
                cnt[uf.size[uf.find(p)]] -= 1
                uf.merge(p - 1, p)
                cnt[uf.size[uf.find(p)]] += 1
            if p < n and uf.size[uf.find(p + 1)] > 0:
                cnt[uf.size[uf.find(p + 1)]] -= 1
                cnt[uf.size[uf.find(p)]] -= 1
                uf.merge(p + 1, p)
                cnt[uf.size[uf.find(p)]] += 1
            if cnt[m]:
                ans = i + 1
        return ans

