class StringHash:
    # 字符串哈希，用O(n)时间预处理，用O(1)时间获取段的哈希值
    def __init__(self, s):
        n = len(s)
        self.BASE = BASE = 131313  # 进制 31,131,13131,13331,131313
        self.MOD = MOD = 10 ** 13 + 7  # 10**13+37 ,10**13+51 ,10**13+99 ,10**13+129 ,10**13+183
        self.h = h = [0] * (n + 1)
        self.p = p = [1] * (n + 1)
        for i in range(1, n + 1):
            p[i] = (p[i - 1] * BASE) % MOD
            h[i] = (h[i - 1] * BASE + ord(s[i - 1])) % MOD

    # 用O(1)时间获取闭区间[l,r]（即s[l:r]）的哈希值，比切片要快
    def get_hash(self, l, r):
        return (self.h[r+1] - self.h[l] * self.p[r - l + 1]) % self.MOD
    

# 判断s是否t的子序列
def isSubsequence(s: str, t: str) -> bool:
    i = 0
    if not s:
        return True
    for c in t:
        if s[i] == c:
            i += 1
            if i == len(s):
                return True
    return False
