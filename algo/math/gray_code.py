# https://leetcode.cn/problems/circular-permutation-in-binary-representation/description/
# 1238. 循环码排列
class Solution:
    def circularPermutation(self, n: int, start: int) -> List[int]:
        # gray code
        # 0, 1出发，每轮将已有的逆序并最高位补1
        # 0, 1. 
        #     -> 0, 1, [11, 10] i=2
        #                    -> 0, 1, 11, 10, [110, 111, 101, 100] i=3
        res = [0, 1]
        start_index = -1
        if start == 0:
            start_index = 0
        elif start == 1:
            start_index = 1
        for i in range(2, n + 1):
            size = len(res)
            for j in range(size - 1, -1, -1):
                add = 1 << (i - 1)
                cur = res[j]
                res.append(cur | add)
                if res[-1] == start:
                    start_index = len(res) - 1
        # 调整顺序，start开头
        return res[start_index:] + res[:start_index]

