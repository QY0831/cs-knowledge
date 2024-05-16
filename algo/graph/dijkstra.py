# Dijkstra 算法模板: 解决单源最短路径问题
# 返回从 start 到每个点的最短路
def dijkstra(g: List[List[Tuple[int]]], start: int) -> List[int]:
    dist = [inf] * len(g)
    dist[start] = 0
    h = [(0, start)]
    while h:
        d, x = heappop(h)
        if d > dist[x]:
            continue
        for y, wt in g[x]:
            new_d = dist[x] + wt
            if new_d < dist[y]:
                dist[y] = new_d
                heappush(h, (new_d, y))
    return dist

# 稠密图：https://leetcode.cn/problems/minimum-cost-of-a-path-with-special-roads/description/
# 求从start到target的最小代价
# 朴素dij（适用于稠密图）
class Solution:
    def minimumCost(self, start: List[int], target: List[int], specialRoads: List[List[int]]) -> int:
        dis = defaultdict(lambda: inf)
        t = tuple(target)
        dis[tuple(start)] = 0 # dis[i]: start到i的最短路
        done = set()
        while True:
            x, dx = None, -1
            # 找到最小dis
            for node, d in dis.items():
                if node not in done and (d < dx or dx == -1):
                    x = node
                    dx = d
            if x == t:
                return dx
            done.add(x)
            a, b = x
            # 根据最小dis，更新
            # 1. 直接跳到终点的距离
            # 2. 跳到特殊路径终点的距离
            dis[t] = min(dis[t], dx + t[0] - a + t[1] - b)
            for x1, y1, x2, y2, cost in specialRoads:
                # 尝试从x到达special road的终点
                s = (x2, y2)
                dis[s] = min(dis[s], dx + abs(x1 - a) + abs(y1 - b) + cost)

# 堆优化dij（适用于稀疏图）
# 例题：
# https://leetcode.cn/problems/network-delay-time/description/
# 共n个节点，从k节点出发，到达最远节点的距离
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        g = [[] for _ in range(n)]  # 邻接表
        for x, y, d in times:
            g[x - 1].append((y - 1, d))

        dis = [inf] * n  # 从k出发，到达各节点的最短距离
        dis[k - 1] = 0
        h = [(0, k - 1)]
        while h:
            dx, x = heappop(h)
            if dx > dis[x]:
                continue
            for y, d in g[x]:  # 更新 x 的邻居的最短路
                new_dis = dx + d
                if new_dis < dis[y]:
                    dis[y] = new_dis
                    heappush(h, (new_dis, y))
        mx = max(dis)
        return mx if mx < inf else -1
    

# 求两个节点间的最短路
# 多源最短路最好用floyd
def shortestPath(n: int, edges: int, node1: int, node2: int) -> int:
    g = [[] for _ in range(n)]  # 邻接表
    for x, y, d in edges:
        g[x].append((y, d))
    dis = [inf] * n
    dis[node1] = 0
    h = [(0, node1)]
    while h:
        dx, x = heappop(h)
        if dx > dis[x]:
            continue
        if x == node2:
            return dx
        for y, d in g[x]:
            new_dis = dx + d
            if new_dis < dis[y]:
                dis[y] = new_dis
                heappush(h, (dis[y], y))
    return -1
