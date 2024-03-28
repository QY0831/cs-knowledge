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
