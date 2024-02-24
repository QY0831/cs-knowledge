# https://leetcode.cn/problems/kth-ancestor-of-a-tree-node/description/
# 获取树节点的第k个祖先
class TreeAncestor:

    def __init__(self, n: int, parent: List[int]):
        m = n.bit_length() - 1
        self.pa = [[p] + [-1] * m for p in parent] # pa[x][i]: x的2^i个祖先
        for i in range(m): # 2^i个祖先
            for x in range(n): # x节点
                # p = A(x, 2^i)
                # A(x, 2^(i+1)) = A(p, 2^(i+1) - 2^i = 2^i)
                p = self.pa[x][i]
                if p != -1:
                    self.pa[x][i+1] = self.pa[p][i]
        
    def getKthAncestor(self, node: int, k: int) -> int:
        # query (10, 5)
        # 5: 101
        for i in range(k.bit_length()):
            if (k >> i) & 1: # 5 & 4 == 1
                node = self.pa[node][i]
                if node == -1:
                    break
        return node