# https://leetcode.cn/problems/number-of-ways-to-earn-points/description/
# 获得分数的方法数
# f[i][j] = sum(f[i-1][j-k*marks]), k=[0, min(count, j // marks)]
class Solution:
    def waysToReachTarget(self, target: int, types: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7
        f = [1] + [0] * target
        for count, marks in types: 
            for j in range(target, 0, -1):
                for k in range(1, min(count, j // marks) + 1):
                    f[j] += f[j - k * marks]
                f[j] %= MOD
        return f[-1]
