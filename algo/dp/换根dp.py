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
  
  
# https://leetcode.cn/problems/time-taken-to-mark-all-nodes/description/
# 3241. 标记所有节点需要的时间
# 需要记录最大、次大深度，以及最大深度方向
class Solution:
    def timeTaken(self, edges: List[List[int]]) -> List[int]:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)
        
        nodes = [None] * n # 保存（最大深度，次大深度，最大深度方向)

        def dfs(x, fa): # 从x出发的最大深度（考虑边权）
            max_d = max_d2 = my = 0
            for y in g[x]:
                if y != fa:
                    depth = dfs(y, x) + 2 - y % 2
                    if depth > max_d:
                        max_d, max_d2 = depth, max_d
                        my = y
                    elif depth > max_d2:
                        max_d2 = depth
            nodes[x] = (max_d, max_d2, my)
            return max_d

        dfs(0, -1)

        ans = [0] * n

        def reroot(x, fa, from_up): # from_up，从fa走得到的路径
            max_d, max_d2, my = nodes[x]
            ans[x] = max(from_up, max_d) # 当前节点的最大深度，或从父节点向上的最大深度
            w = 2 - x % 2 # y -> x的边权
            for y in g[x]:
                if y != fa:
                    # 1.from_up可能为x节点的from_up + w
                    # 2.如果y在x出发的最大深度的路径上，则from_up可能是max_d2 + w, 否则max_d + w
                    # 两者取max
                    reroot(y, x, w + max(from_up, max_d2 if y == my else max_d))

        reroot(0, -1, 0)
        return ans
                