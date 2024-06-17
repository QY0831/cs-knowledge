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



# 利用并查集合并区间
# https://leetcode.cn/problems/find-latest-group-of-size-m/
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
