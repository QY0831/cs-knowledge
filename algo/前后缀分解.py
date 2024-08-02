# 基本思路：
# 两次循环求pre数组和suf数组，然后遍历取最值
# pre[i]表示以i结尾满足条件的cost, suf[i]表示以i开头满足条件的cost

# https://leetcode.cn/problems/find-good-days-to-rob-the-bank/
# 2100. 适合野炊的日子
# rating: 1702
class Solution:
    def goodDaysToRobBank(self, security: List[int], time: int) -> List[int]:
        n = len(security)
        pre = [0] * n
        for i in range(1, n):
            if security[i] <= security[i-1]:
                pre[i] = pre[i-1] + 1
        
        suf = 0
        ans = []
        for i in range(n - 1, time - 1, -1):
            if i != n - 1 and security[i] <= security[i+1]:
                suf += 1
            else:
                suf = 0
            if pre[i] >= time and suf >= time:
                ans.append(i)
        return ans


# https://leetcode.cn/problems/minimum-cost-to-make-all-characters-equal/
# 2712. 使所有字符相等的最小成本
# rating: 1791
class Solution:
    def minimumCost(self, s: str) -> int:
        n = len(s)
        pre = [inf] * n
        pre[0] = 0
        for i in range(1, n):
            if s[i] == s[i - 1]:
                pre[i] = pre[i - 1]
            else:
                pre[i] = pre[i - 1] + i
        
        ans = pre[-1]
        suf = 0
        for i in range(n - 2, -1, -1):
            if s[i] != s[i + 1]:
                suf += n - i - 1
            ans = min(ans, pre[i] + suf)
        return ans

