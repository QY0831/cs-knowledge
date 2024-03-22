class UnionFind:
    def __init__(self, n, size=None):
        self.parent = list(range(n))
        self.size = [1] * n if size is None else size

    def find(self, a):
        if self.parent[a] != a:
            self.parent[a] = self.find(self.parent[a])
        return self.parent[a]

    def merge(self, a, b):
        pa, pb = self.find(a), self.find(b)
        if pa == pb: return False
        self.parent[pb] = pa
        self.size[pa] += self.size[pb]
        return True

    def getSize(self, a):
        return self.size[self.find(a)]
