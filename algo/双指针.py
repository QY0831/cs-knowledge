# https://leetcode.cn/problems/swap-for-longest-repeated-character-substring/
# 1156. 单字符重复子串的最大长度
# rating: 1787
class Solution:
    def maxRepOpt1(self, text: str) -> int:
        cnt = Counter(text)
        i = ans = 0
        n = len(text)
        while i < n:
            j = i
            while j < n and text[j] == text[i]:
                j += 1
            l = j - i # 连续长度
            k = j + 1 # 跳过一个不同字符
            while k < n and text[k] == text[i]:
                k += 1
            r = k - j - 1 # 连续长度
            # 替换text[j]以连接两段，长度上限是cnt[text[i]]
            ans = max(ans, min(cnt[text[i]], l + r + 1))
            i = j
        return ans
