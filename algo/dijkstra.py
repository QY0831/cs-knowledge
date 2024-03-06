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


# https://leetcode.cn/problems/network-delay-time/description/
# 朴素dij（适用于稠密图）
# 稠密图：https://leetcode.cn/problems/minimum-cost-of-a-path-with-special-roads/description/
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        g = [[] for _ in range(n)]  # 邻接表
        for x, y, d in times:
            g[x - 1].append((y - 1, d))

        dis = [inf] * n # dis[i] 到达i的最短路径
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

# 堆优化dij（适用于稀疏图）
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        g = [[] for _ in range(n)]  # 邻接表
        for x, y, d in times:
            g[x - 1].append((y - 1, d))

        dis = [inf] * n
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
