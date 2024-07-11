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

# 判断回文
def is_palindrome(s: str) -> bool:
    i = 0
    j = len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True

# 得到所有回文子串
class Solution(object):
    def __init__(self):
        self.ans = 0
    
    def countSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """
        # 以每个位置作为回文中心，尝试扩展
        # 回文中心有2种形式，1个数或2个数
        n = len(s)
        
        def spread(left, right):
            while left >= 0 and right <= n-1 and s[left] == s[right]:
                left -= 1
                right += 1
                self.ans += 1
        
        for i in range(n):
            spread(i, i)
            spread(i, i+1)
        
        return self.ans

class StringHash:
    # 字符串哈希，用O(n)时间预处理，用O(1)时间获取段的哈希值
    def __init__(self, s):
        n = len(s)
        self.BASE = BASE = 131313  # 进制 31,131,13131,13331,131313
        self.MOD = MOD = 10 ** 13 + 7  # 10**13+37 ,10**13+51 ,10**13+99 ,10**13+129 ,10**13+183
        # 卡常时尝试：MOD = 121499449， 并调小BASE  
        self.h = h = [0] * (n + 1)
        self.p = p = [1] * (n + 1)
        for i in range(1, n + 1):
            p[i] = (p[i - 1] * BASE) % MOD
            h[i] = (h[i - 1] * BASE + ord(s[i - 1])) % MOD

    # 用O(1)时间获取闭区间[l,r]（即s[l:r+1]）的哈希值，比切片要快
    def get_hash(self, l, r):
        return (self.h[r+1] - self.h[l] * self.p[r - l + 1]) % self.MOD
    

# https://leetcode.cn/problems/construct-string-with-minimum-cost/description/
# 3213. 最小代价构造字符串
class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        n = len(target)
        min_cost = defaultdict(lambda: inf)
        for w, c in zip(words, costs):
            h = StringHash(w).h[-1]
            min_cost[h] = min(min_cost[h], c)
        sh = StringHash(target)
        f = [0] + [inf] * n

        sorted_lens = sorted(set(map(len, words)))

        for i in range(1, n + 1):
            for sl in sorted_lens:
                if sl > i:
                    break
                sub_hash = sh.get_hash(i - sl, i - 1)
                res = f[i - sl] + min_cost[sub_hash]
                if res < f[i]:
                    f[i] = res
        return -1 if f[n] == inf else f[n]
