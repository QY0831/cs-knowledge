# https://leetcode.cn/problems/count-of-integers/?envType=list&envId=VyVp7NFA
MOD = 10 ** 9 + 7
class Solution:
    def count(self, num1: str, num2: str, min_sum: int, max_sum: int) -> int:

        def compute(s):
            
            @cache
            def dfs(i, is_num, is_limit, sum_):
                if i == len(s):
                    return int(is_num and min_sum <= sum_ <= max_sum)
                
                res = 0
                if not is_num:
                    res += dfs(i + 1, False, False, 0)
                
                up = int(s[i]) if is_limit else 9
                lo = 0 if is_num else 1

                for d in range(lo, up + 1):
                    res += dfs(i + 1, True, is_limit and d == up, sum_ + d)
                
                return res % MOD
            
            return dfs(0, False, True, 0)
        
        return (compute(num2) - compute(str(int(num1) - 1))) % MOD