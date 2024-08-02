# 建图
graph = collections.defaultdict(set)
for a, b in edges:
    graph[a].add(b)
    graph[b].add(a)


# 二叉树建图（节点val不重复）
g = defaultdict(list)
def dfs(node, fa):
    if fa:
        g[node.val].append(fa.val)
    if node.left:
        g[node.val].append(node.left.val)
        dfs(node.left, node)
    if node.right:
        g[node.val].append(node.right.val)
        dfs(node.right, node)
dfs(root, None)


# 二叉树保存parents
parents = {}
def dfs(node: Optional[TreeNode], pa: Optional[TreeNode]) -> None:
    if node is None: return
    parents[node] = pa
    dfs(node.left, node)
    dfs(node.right, node)
dfs(root, None)


# 朴素BFS
def search(start, target):
    q = deque([start])
    seen = {start}
    while q:
        node = q.popleft()
        if node == target:
            return
        for nxt_node in graph[node]:
            if nxt_node not in seen:
                q.append(nxt_node)
                seen.add(nxt_node)
    

# 多源BFS
# https://leetcode.cn/problems/as-far-from-land-as-possible/
class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:
        q = deque([])
        seen = set()
        n = len(grid)
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    q.append((i, j))
                    seen.add((i, j))
        ans = -1
        dis = 0
        while q:
            size = len(q)
            for _ in range(size):
                x, y = q.popleft()
                if grid[x][y] == 0:
                    ans = max(ans, dis)
                for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in seen:
                        q.append((nx, ny))
                        seen.add((nx, ny))
            dis += 1
        return ans 


# 多源BFS
# https://leetcode.cn/problems/map-of-highest-peak/description/
# 1765. 地图中的最高点
class Solution:
    def highestPeak(self, isWater: List[List[int]]) -> List[List[int]]:
        m = len(isWater)
        n = len(isWater[0])
        ans = [[-1] * n for _ in range(m)]
        q = deque([])
        for i in range(m):
            for j in range(n):
                if isWater[i][j]:
                    q.append((i, j))
                    ans[i][j] = 0
        h = 1
        while q:
            size = len(q)
            for _ in range(size):
                x, y = q.popleft()
                for px, py in (1,0),(0,1),(-1,0),(0,-1):
                    nx, ny = x + px, y + py
                    if nx < 0 or nx >= m or ny < 0 or ny >= n:
                        continue
                    if ans[nx][ny] == -1:
                        ans[nx][ny] = h
                        q.append((nx, ny))
            h += 1
        return ans
        

# 拓扑排序
# 建图 + 记录入度
# 入度为0入队 -> 弹出 -> 更新入度，入度为0的入队 -> 弹出 ->  ...
# https://leetcode.cn/problems/course-schedule/description/
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        ind = [0] * numCourses
        outd = [[] for _ in range(numCourses)]

        for c, pre in prerequisites:
            ind[c] += 1
            outd[pre].append(c)
        
        q = deque([])
        for i in range(numCourses):
            if ind[i] == 0:
                q.append(i)

        cnt = 0
        while q:
            c = q.popleft()
            cnt += 1
            for nxt in outd[c]:
                ind[nxt] -= 1
                if ind[nxt] == 0:
                    q.append(nxt)
        return cnt == numCourses


# BFS求次最短路
# https://leetcode.cn/problems/second-minimum-time-to-reach-destination
class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:
        graph = collections.defaultdict(set)
        for start, end in edges:
            graph[start].add(end)
            graph[end].add(start)

        # i: 1 ~ n
        # dist[i][0]:  1 ~ i 最短距离
        # dist[i][1]:  1 ~ i 次短距离
        dist = [[float('inf')] * 2 for _ in range(n+1)]
        dist[1][0] = 0
        q = collections.deque([])
        q.append((1, 0))  # position, distance
        while dist[n][1] == float('inf'):
            position, distance = q.popleft()
            for next in graph[position]:
                d = distance + 1
                if d < dist[next][0]:
                    dist[next][0] = d
                    q.append((next, d))
                elif dist[next][0] < d < dist[next][1]:
                    dist[next][1] = d
                    q.append((next, d))
                    
        ans = 0
        # time 3
        # change 5
        # green:0 red:5 green:10 red:15 green:20
        # dist = 3
        # 3 + 3 + (10-6) + 3
        for _ in range(dist[n][1]):
            if ans % (change * 2) >= change:
                ans += change * 2 - ans % (change * 2)
            ans += time
        return ans
    

# BFS找最小环
# https://leetcode.cn/problems/shortest-cycle-in-a-graph/
class Solution:
    def findShortestCycle(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)

        # 枚举所有边，每一次把边 u-v 删除，
        # 然后求从 u 出发，不经过 u−v 到达 v 的最短路。
        # 这条最短路，加上被删掉的边 u−v 就是一个环
        def bfs(u, v):
            q = deque([u])
            vis = [False] * n
            vis[u] = True
            step = 0
            while q:
                size = len(q)
                for _ in range(size):
                    x = q.popleft()
                    if x == v:
                        return step + 1
                    for y in g[x]:
                        if vis[y]:
                            continue
                        if x == u and y == v:
                            continue
                        q.append(y)
                        vis[y] = True
                step += 1
            return inf
        
        ans = min(bfs(u, v) for u, v in edges)
        return ans if ans != inf else -1
