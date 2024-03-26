# Trie (前缀树)
class Node:
    __slots__ = 'son', 'cnt' # 根据题意，增加属性
    
    def __init__(self):
        self.son = [None] * 26
        self.cnt = 0

class Trie:

    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        cur = self.root
        for c in word:
            cid = ord(c) - ord('a')
            if cur.son[cid] is None:
                cur.son[cid] = Node()
            cur = cur.son[cid]
        cur.cnt += 1

    def search(self, word: str) -> bool:
        cur = self.root
        for c in word:
            cid = ord(c) - ord('a')
            if cur.son[cid] is None:
                return False
            cur = cur.son[cid]
        return cur.cnt > 0

    def startsWith(self, prefix: str) -> bool:
        cur = self.root
        for c in prefix:
            cid = ord(c) - ord('a')
            if cur.son[cid] is None:
                return False
            cur = cur.son[cid]
        return True


# 最长公共后缀查询
# https://leetcode.cn/problems/longest-common-suffix-queries/description/
class Node:
    __slots__ = 'son', 'min_l', 'i'

    def __init__(self):
        self.son = [None] * 26
        self.min_l = inf

class Solution:
    def stringIndices(self, wordsContainer: List[str], wordsQuery: List[str]) -> List[int]:
        root = Node()
        for i, s in enumerate(wordsContainer):
            cur = root
            if len(s) < cur.min_l:
                cur.min_l, cur.i = len(s), i # 这棵树最短的字符串及下标
            for c in s[::-1]:
                cid = ord(c) - ord('a')
                if cur.son[cid] is None:
                    cur.son[cid] = Node()
                cur = cur.son[cid]
                if len(s) < cur.min_l: # 更新该前缀最短的字符串及下标
                    cur.min_l = len(s)
                    cur.i = i
        
        ans = []
        for s in wordsQuery:
            cur = root
            for c in s[::-1]:
                cid = ord(c) - ord('a')
                if cur.son[cid] is None:
                    break
                cur = cur.son[cid]
            ans.append(cur.i)
        return ans
    

# https://leetcode.cn/problems/palindrome-pairs/
# 找word1, word2组成回文串
class Node:

    __slots__ = 'son', 'end', 'idx'

    def __init__(self):
        self.son = [None] * 27  # son[26] = ""
        self.end = False

class Solution:
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        pre_root = Node()
        for i, word in enumerate(words):
            if word == "":
                pre_root.son[-1] = Node()
                pre_root.son[-1].end = True
                pre_root.son[-1].idx = i
                continue
            cur = pre_root
            for c in word:
                cid = ord(c) - ord('a')
                if cur.son[cid] is None:
                    cur.son[cid] = Node()
                cur = cur.son[cid]
            cur.end = True
            cur.idx = i
        
        suf_root = Node() 
        for i, word in enumerate(words):
            if word == "":
                continue
            cur = suf_root
            for c in reversed(word):
                cid = ord(c) - ord('a')
                if cur.son[cid] is None:
                    cur.son[cid] = Node()
                cur = cur.son[cid]
            cur.end = True
            cur.idx = i

        def valid(s, i, j):
            while i < j:
                if s[i] != s[j]:
                    return False
                i += 1
                j -= 1
            return True
        
        ans = []
        for i, word in enumerate(words):
            if word == "":
                continue
            m = len(word)
            # 搜索 “”
            if pre_root.son[-1] is not None and valid(word, 0, m - 1):
                ans.append([i, pre_root.son[-1].idx])
                ans.append([pre_root.son[-1].idx, i])
            
            # 单词放左边：abcb + a
            # 从后缀树搜 a,ab,abc,abcb
            cur = suf_root
            for j in range(m):
                letter_id = ord(word[j]) - ord('a')
                if cur.son[letter_id] is not None:
                    cur = cur.son[letter_id]
                else:
                    break
                if cur.end and valid(word, j+1, m-1) and i != cur.idx:
                    ans.append([i, cur.idx])
            
            # 单词放右边：a + bcda
            # 从前缀树搜 a,ad,adc,adcb(这个不搜，会重复)
            cur = pre_root
            for j in range(m - 1, 0, -1):
                letter_id = ord(word[j]) - ord('a')
                if cur.son[letter_id] is not None:
                    cur = cur.son[letter_id]
                else:
                    break
                if cur.end and valid(word, 0, j-1):
                    ans.append([cur.idx, i])
        return ans
    

# https://leetcode.cn/problems/prefix-and-suffix-search/description/
# 前缀后缀搜索
class Node:
    __slots__ = 'son', 'idx_list' # 根据题意，增加属性
    
    def __init__(self):
        self.son = [None] * 26
        self.idx_list = []

class WordFilter:

    def __init__(self, words: List[str]):
        self.pre_root = Node()
        self.suf_root = Node()
        for i, word in enumerate(words):
            self.insert(self.pre_root, i, word)
            self.insert(self.suf_root, i, word[::-1])

    def insert(self, root, idx: int, word: str) -> None:
        cur = root
        for c in word:
            cid = ord(c) - ord('a')
            if cur.son[cid] is None:
                cur.son[cid] = Node()
            cur = cur.son[cid]
            cur.idx_list.append(idx)

    def search(self, root, word: str) -> bool:
        cur = root
        for c in word:
            cid = ord(c) - ord('a')
            if cur.son[cid] is None:
                return None
            cur = cur.son[cid]
        return cur.idx_list

    def f(self, pref: str, suff: str) -> int:
        r1 = self.search(self.pre_root, pref)
        if not r1: 
            return -1
        r2 = self.search(self.suf_root, suff[::-1])
        if not r2: 
            return -1
        i = len(r1) - 1
        j = len(r2) - 1
        while i >= 0 and j >= 0:
            if r1[i] > r2[j]:
                i -= 1
            elif r1[i] < r2[j]:
                j -= 1
            else:
                return r1[i]
        return -1

