# https://leetcode.cn/problems/network-delay-time/description/
# 朴素dij
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


# 堆优化dij
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
