# https://leetcode.cn/problems/find-good-days-to-rob-the-bank/
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
