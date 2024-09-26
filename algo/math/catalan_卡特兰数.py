# Catalan 数是一系列整数，常用于解决与递归结构相关的组合数学问题，包括不相交配对、二叉树结构、括号匹配等。

def catalan_number(n):
    if n == 0:
        return 1
    catalan = [0] * (n + 1)
    catalan[0] = 1
    
    for i in range(1, n + 1): # C[i]: i次握手的方案数
        for j in range(i): # 考虑第一个握手将圈分成两部分, 第一部分有j次握手，第二部分有i - j - 1次握手
            catalan[i] += catalan[j] * catalan[i - j - 1]
            catalan[i] %= 1_000_000_007
    
    return catalan[n] % 1_000_000_007


# https://leetcode.cn/problems/handshakes-that-dont-cross/description/
# 1259. 不相交的握手
# rating: 1951
class Solution:
    def numberOfWays(self, numPeople: int) -> int:
        return catalan_number(numPeople // 2) 
