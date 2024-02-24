# 标准kmp
# 返回pattern在text中出现的所有位置
def kmp(text, pattern):
    m = len(pattern)
    max_len = 0
    match = [0] * m
    for i in range(1, m):
        while max_len > 0 and pattern[i] != pattern[max_len]:
            max_len = match[max_len - 1]
        if pattern[i] == pattern[max_len]:
            max_len += 1
        match[i] = max_len

    res = []
    count = 0
    for i, v in enumerate(text):
        while count > 0 and v != pattern[count]:
            count = match[count - 1]
        if v == pattern[count]:
            count += 1
        if count == m:
            res.append(i - m + 1)
            count = match[count - 1]
    return res

# Z函数：扩展kmp
# z[i]表示s和s[i,n-1]的最长公共前缀（LCP）的长度
def get_z(s):
    l = r = 0
    n = len(s)
    z = [0] * n
    for i in range(1, n):
        if z[i - l] < r - i + 1:
            z[i] = z[i - l]
        else:
            z[i] = max(r - i + 1, 0) # 考虑i > r的情况
            while (i + z[i] < n and s[i + z[i]] == s[z[i]]):
                z[i] += 1
            l = i
            r = i + z[i] - 1
    # z[0] = n 某些情况需要
    return z