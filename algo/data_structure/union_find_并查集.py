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
        return "\n".join(f"{root}: {member}" for root, member in self.get_groups().items())

    def __len__(self) -> int:
        return self.part


class UnionFindRange:
    __slots__ = "part", "_n", "_parent", "_rank"

    def __init__(self, n: int):
        self.part = n
        self._n = n
        self._parent = list(range(n))
        self._rank = [1] * n

    def find(self, x: int) -> int:
        while x != self._parent[x]:
            self._parent[x] = self._parent[self._parent[x]]
            x = self._parent[x]
        return x

    def union(
        self, x: int, y: int, beforeMerge: Optional[Callable[[int, int], None]] = None
    ) -> bool:
        """union后, 大的编号所在的组的指向小的编号所在的组(向左合并)."""
        if x < y:
            x, y = y, x
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX == rootY:
            return False
        if beforeMerge is not None:
            beforeMerge(rootY, rootX)
        self._parent[rootX] = rootY
        self._rank[rootY] += self._rank[rootX]
        self.part -= 1
        return True

    def unionRange(
        self, left: int, right: int, beforeMerge: Optional[Callable[[int, int], None]] = None
    ) -> int:
        """合并[left,right]区间, 返回合并次数."""
        if left >= right:
            return 0
        leftRoot = self.find(left)
        rightRoot = self.find(right)
        unionCount = 0
        while rightRoot != leftRoot:
            unionCount += 1
            self.union(rightRoot, rightRoot - 1, beforeMerge)
            rightRoot = self.find(rightRoot - 1)
        return unionCount

    def isConnected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def getSize(self, x: int) -> int:
        return self._rank[self.find(x)]


# https://leetcode.cn/problems/count-the-number-of-complete-components/description/
# 2685. 统计完全连通分量的数量
# rating: 1769
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
# rating: 1928
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


# https://leetcode.cn/problems/check-if-the-rectangle-corner-is-reachable/description/
# 3235. 判断矩形的两个角落是否可达
# 判断是否有一条路径从左上角到右下角，不经过任何圆的内部和边界
# 解法：判断左上边界和右下边界是否连通
class Solution:
    def canReachCorner(self, X: int, Y: int, circles: List[List[int]]) -> bool:
        # n个圆标记为 0...n-1
        # 上边界+左边界标记为 n
        # 下边界+右边界标记为 n+1
        # 并查集连边，判断n,n+1是否连通
        n = len(circles)
        uf = UnionFind(n + 2)
        for i, (ox, oy, r) in enumerate(circles):
            if ox <= r or oy + r >= Y: # 与左或上连通
                uf.merge(i, n)
            if ox + r >= X or oy <= r: # 与下或右连通
                uf.merge(i, n+1)
            for j in range(i + 1, n):
                # 与其他圆相交或相切: 圆心距离 <= 半径距离之和
                qx, qy, qr = circles[j]
                if (ox - qx) * (ox - qx) + (oy - qy) * (oy - qy) <= (r + qr) * (r + qr):
                    uf.merge(i, j)
            if uf.is_connected(n, n + 1):
                return False
        return True


# https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-ii/description/
# 3244. 新增道路查询后的最短距离 II
# 区间并查集
# 类似：https://leetcode.cn/problems/amount-of-new-area-painted-each-day/description/
class UnionFind:
    def __init__(self, n):
        self.n = n
        self.parent = list(range(n))
        self.part = n # 连通分量

    def find(self, a):
        if self.parent[a] != a:
            self.parent[a] = self.find(self.parent[a])
        return self.parent[a]

    def merge(self, a, b):
        pa, pb = self.find(a), self.find(b)
        if pa == pb: 
            return False
        self.parent[pa] = pb
        self.part -= 1
        return True
    
class Solution:
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        # 01->0
        # 12->1
        # ..
        # n-1,n -> n - 1
        uf = UnionFind(n - 1)
        ans = []
        for a, b in queries:
            l = uf.find(a)
            r = uf.find(b - 1)
            while l != r:
                uf.merge(r, r - 1) # 向左合并
                r = uf.find(r - 1)
            ans.append(uf.part)
        return ans


# https://leetcode.cn/problems/last-day-where-you-can-still-cross/description/
# 1970. 你能穿过矩阵的最后一天
# 倒序并查集
# rating: 2123
class Solution:
    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        n = row * col
        uf = UnionFind(n + 2) # n: top n+1: bot

        def get_idx(i, j):
            return i * col + j

        s = set() 
        for i in range(len(cells) - 1, -1, -1):
            x, y = cells[i]
            x -= 1
            y -= 1
            k = get_idx(x, y)

            for dx, dy in (0, 1), (0, -1), (1, 0), (-1, 0):
                nx, ny = x + dx, y + dy
                if 0 <= nx < row and 0 <= ny < col and (nx, ny) in s:
                    uf.merge(k, get_idx(nx, ny))
            
            if x + 1 == row:
                uf.merge(k, n + 1)
            if x == 0:
                uf.merge(k, n)

            s.add((x, y))

            if uf.is_connected(n, n + 1):
                return i
