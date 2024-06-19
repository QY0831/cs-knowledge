def isSubsequence(s: str, t: str) -> bool: # 判断s是否是t的子序列
    if not s:
        return True
    m = len(s)
    n = len(t)
    i = 0
    for j in range(n):
        if s[i] == t[j]:
            i += 1
            if i == m:
                return True
    return False

print(isSubsequence("abc", "ahbgdc")) # True
