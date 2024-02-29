# 套路：先计算根结点的答案，换根后根据状态变化向下得到根节点儿子的答案，向下递推出所有答案。
# https://leetcode.cn/problems/sum-of-distances-in-tree
class Solution:
    def sumOfDistancesInTree(self, n: int, edges: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)
        
        size = [1] * n # size[i] 子树i的大小
        ans = [0] * n

        def dfs(x, fa, depth):
            ans[0] += depth # 统计根节点0到所有其他节点的距离
            for nxt in g[x]:
                if nxt != fa:
                    dfs(nxt, x, depth + 1) # 统计子树大小
                    size[x] += size[nxt] # 累加子树大小
        dfs(0, -1, 0)

        # 已知ans[0]，可求0的子节点的ans
        # 向下递推可求所有ans
        # ans[y] = ans[x] + n - size[y] - size[y]
        # 对于y，从x换到y，到达子树y所有节点的距离-1，所以-size[y]
        # 到达其他节点的距离+1，所以+ n - size[y]
        # ans[y] = ans[x] + n - 2 * size[y]

        def reroot(x, fa):
            for y in g[x]:
                if y != fa:
                    ans[y] = ans[x] + n - 2 * size[y]
                    reroot(y, x)
        reroot(0, -1)
        return ans


# https://leetcode.cn/problems/count-number-of-possible-root-nodes/
"""
1. 得到以0为根的猜对次数 cnt0
2. cnt1 = cnt0 - ((0, 1) in guesses) + ((1, 0) in guesses)
"""
class Solution:
    def rootCount(self, edges: List[List[int]], guesses: List[List[int]], k: int) -> int:
      g = [[] for _ in range(len(edges) + 1)] 
      for a, b in edges:
        g[a].append(b)
        g[b].append(a)

      s = {(x, y) for x, y in guesses}

      # init dfs
      # 得到以0为根时的猜对次数
      cnt0 = 0
      def dfs(x: int, fa: int) -> None:
        nonlocal cnt0
        for y in g[x]:
            if y != fa:
                cnt0 += (x, y) in s  # 以 0 为根时，猜对了
                dfs(y, x)
      dfs(0, -1)

      ans = 0
      def reroot(x: int, fa: int, cnt: int) -> None:
        nonlocal ans
        if cnt >= k:  # 此时 cnt 就是以 x 为根时的猜对次数
            ans += 1
        for y in g[x]:
            if y != fa:
                reroot(y, x, cnt - ((x, y) in s) + ((y, x) in s))

      reroot(0, -1, cnt0)
      return ans