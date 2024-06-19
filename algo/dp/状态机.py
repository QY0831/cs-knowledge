# 一般定义f[i][j]为前缀a[:i]在状态j下的最优值。一般j很小，可以通过维护几个状态来优化空间。
# 经典题目是【买卖股票】系列

# https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/description/
# 买卖股票的最佳时机 III
# 最多可以完成 两笔 交易
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        buy1 = buy2 = -prices[0]
        sell1 = sell2 = 0
        for i in range(1, len(prices)):
            buy1 = max(buy1, -prices[i])
            sell1 = max(sell1, buy1 + prices[i])
            buy2 = max(buy2, sell1 - prices[i])
            sell2 = max(sell2, buy2 + prices[i])
        return sell2


# https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/description/
# 买卖股票的最佳时机 IV
# 最多可以完成 k 笔交易
class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        buy = [-prices[0] for _ in range(k)]
        sell = [0 for _ in range(k)]
        n = len(prices)
        for i in range(1, n):
            for j in range(k):
                buy[j] = max(buy[j], sell[j-1]-prices[i] if j > 0 else -prices[i])
                sell[j] = max(sell[j], buy[j]+prices[i])
        return sell[-1]


# https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/
# 买卖股票的最佳时机含冷冻期
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
    	# p = prices[i]
        # f[i][0]: buyed = max(f[i-1][0], f[i-1][2] - p)
        # f[i][1]: sold = max(f[i-1][1], f[i-1][0] + p)
        # f[i][2]: skip = max(f[i-1][0], f[i-1][1], f[i-1][2])
        f0, f1, f2 = -prices[0], 0, 0
        for i in range(1, len(prices)):
            p = prices[i]
            f0, f1, f2 = max(f0, f2 - p), max(f1, f0 + p), max(f0, f1, f2)
        return max(f0, f1, f2)


# https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/
# 买卖股票的最佳时机含手续费
class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        # p = prices[i]
        # f[i][0]: buyed = max(f[i-1][0], f[i-1][1] - p)
        # f[i][1]: sold = max(f[i-1][1], f[i-1][0] + p - fee)
        f0, f1 = -prices[0], 0
        for i in range(1, len(prices)):
            p = prices[i]
            f0, f1 = max(f0, f1 - p), max(f1, f0 + p - fee)
        return f1

