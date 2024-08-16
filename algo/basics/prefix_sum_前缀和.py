# 一维前缀和
pre = list(accumulate(arr, initial=0)) 
# sum[i, j] = pre[j+1] - pre[i]
# sum(i, j) = pre[j] - pre[i+1]

# 二维前缀和
m = len(grid)
n = len(grid[0])
pre_sum = [[0] * (n+1) for _ in range(m+1)]
ans = 0
for i in range(1, m+1):
    for j in range(1, n+1):
        pre_sum[i][j] = pre_sum[i-1][j] + pre_sum[i][j-1] - pre_sum[i-1][j-1] + grid[i-1][j-1]
        

class PreFixSumMatrix:
    def __init__(self, mat):
        self.mat = mat
        self.m, self.n = len(mat), len(mat[0])
        self.pre = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        for i in range(self.m):
            for j in range(self.n):
                self.pre[i + 1][j + 1] = self.pre[i][j + 1] + self.pre[i + 1][j] - self.pre[i][j] + mat[i][j]
        return

    def query(self, xa: int, ya: int, xb: int, yb: int) -> int:
        """left up corner is (xa, ya) and right down corner is (xb, yb)"""
        assert 0 <= xa <= xb <= self.m - 1
        assert 0 <= ya <= yb <= self.n - 1
        return self.pre[xb + 1][yb + 1] - self.pre[xb + 1][ya] - self.pre[xa][yb + 1] + self.pre[xa][ya]