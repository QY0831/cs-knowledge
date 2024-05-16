# floyd: 解决多源最短路
def shortested_path(edges, n):
    w = [[inf] * n for _ in range(n)]
    for x, y, wt in edges: 
        w[x][y] = w[y][x] = wt # 注意是否有向

    f = w
    # f[k][i][j] = min(f[k-1][i][j], f[k][i][k] + f[k][k][j])
    for k in range(n):
        for i in range(n):
            for j in range(n):
                f[i][j] = min(f[i][j], f[i][k] + f[k][j])
    # f[i][j]: i到j的最短路
    return f


# https://leetcode.cn/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance
class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        
        w = [[inf] * n for _ in range(n)]
        for a, b, wt in edges:
            w[a][b] = w[b][a] = wt

        f = w
        # f[k][i][j] = min(f[k-1][i][j], f[k][i][k] + f[k][k][j])
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    f[i][j] = min(f[i][j], f[i][k] + f[k][j])
            
        ans = 0
        min_cnt = inf
        for i in range(n):
            cnt = 0
            for j in range(n):
                if j != i and f[i][j] <= distanceThreshold:
                    cnt += 1
            if cnt <= min_cnt:
                min_cnt = cnt
                ans = i
        return ans
