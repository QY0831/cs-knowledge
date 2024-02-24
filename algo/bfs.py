# 建图
graph = collections.defaultdict(set)
for a, b in edges:
    graph[a].add(b)
    graph[b].add(a)

# 朴素广搜
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
    

# 多源广搜
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

