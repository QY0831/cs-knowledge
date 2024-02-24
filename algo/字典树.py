class Node:
    __slots__ = 'son', 'cnt'

    def __init__(self):
        self.son = dict()
        self.cnt = 0

words = ["apple", "april", "algorithm"]
root = Node()
for t in words: 
    cur = root
    for i, c in enumerate(t):
        if c not in cur.son:
            cur.son[c] = Node()
        cur = cur.son[c]
    cur.cnt += 1