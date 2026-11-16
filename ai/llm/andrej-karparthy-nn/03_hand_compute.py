# -*- coding: utf-8 -*-
"""
03.ipynb 的 forward / backward 手算版
=====================================
把 notebook 里的网络缩到最小规模，用纯 Python 手动实现每一步，
并用「数值微分(有限差分)」验证手推的梯度是否正确。

与原 notebook 的对应关系：
    emb     = C[X]                          # (1,3,2)
    h       = tanh(emb.view(-1,6) @ W1 + b1) # (1,2)
    logits  = h @ W2 + b2                   # (1,3)
    probs   = softmax(logits)
    loss    = -log(probs[0, Y])

这里取：词表 3 个字符，上下文 3，embedding 维 2 -> 输入 6 维
      隐藏层 2 个神经元，输出 3 类。
"""
import math
import sys
sys.stdout.reconfigure(encoding="utf-8")

# ---------------- 权重（故意选整齐的小数，方便手算/手绘） ----------------
C = [
    [0.5, -0.5],   # 字符 0 'a' 的 embedding
    [1.0,  0.5],   # 字符 1 'b'
    [-0.5, 1.0],   # 字符 2 'c'
]

W1 = [
    [ 0.5, -1.0],  # 输入特征 0 到两个隐藏神经元的权重
    [ 1.0,  0.5],  # 特征 1
    [-0.5,  0.5],  # 特征 2
    [ 0.5,  1.0],  # 特征 3
    [-1.0, -0.5],  # 特征 4
    [ 0.5,  0.5],  # 特征 5
]
b1 = [0.1, -0.2]

W2 = [
    [ 0.5, -0.5,  1.0],  # 隐藏 0 -> 3 个 logit
    [-1.0,  0.5, -0.5],  # 隐藏 1 -> 3 个 logit
]
b2 = [0.0, 0.1, -0.1]

# 一个样本：上下文 [a, b, c]，目标预测字符 0 ('a')
X = [0, 1, 2]
Y = 0


# ---------------- FORWARD ----------------
def forward():
    # 1) embedding 查表: emb[i] = C[X[i]]
    emb = [C[x][:] for x in X]                      # 3 行 x 2 列
    # 2) 展平成 6 维
    flat = [v for row in emb for v in row]          # [e00,e01,e10,e11,e20,e21]
    # 3) 隐藏层 pre-activation
    pre = [0.0, 0.0]
    for j in range(2):
        s = b1[j]
        for k in range(6):
            s += flat[k] * W1[k][j]
        pre[j] = s
    # 4) tanh
    h = [math.tanh(p) for p in pre]
    # 5) logits
    logits = [0.0, 0.0, 0.0]
    for t in range(3):
        s = b2[t]
        for j in range(2):
            s += h[j] * W2[j][t]
        logits[t] = s
    # 6) softmax
    counts = [math.exp(l) for l in logits]
    z = sum(counts)
    probs = [c / z for c in counts]
    # 7) cross entropy loss
    loss = -math.log(probs[Y])
    return emb, flat, pre, h, logits, counts, probs, loss


emb, flat, pre, h, logits, counts, probs, loss = forward()

print("=" * 60)
print("FORWARD（前向）")
print("=" * 60)
print(f"X = {X}  (上下文 a,b,c)")
print(f"Y = {Y}  (目标字符 a)")
print()
print("emb = C[X]  (3 行 x 2 列):")
for i, row in enumerate(emb):
    print(f"  emb[{i}] = {row}")
print(f"flat = emb 展平 = {flat}")
print()
print("pre = flat·W1 + b1:")
print(f"  pre[0] = {pre[0]:.6f}")
print(f"  pre[1] = {pre[1]:.6f}")
print(f"h = tanh(pre):")
print(f"  h[0] = {h[0]:.6f}")
print(f"  h[1] = {h[1]:.6f}")
print(f"logits = h·W2 + b2 = {[f'{l:.6f}' for l in logits]}")
print(f"counts = exp(logits) = {[f'{c:.6f}' for c in counts]}")
print(f"probs = softmax = {[f'{p:.6f}' for p in probs]}")
print(f"loss = -log(probs[0]) = {loss:.6f}")


# ---------------- BACKWARD ----------------
def backward(flat, pre, h, probs):
    # d loss / d probs：只有目标位置非零
    dprobs = [0.0, 0.0, 0.0]
    dprobs[Y] = -1.0 / probs[Y]

    # softmax:  dlogits[t] = probs[t] - (t==Y ? 1 : 0)
    dlogits = [probs[t] - (1.0 if t == Y else 0.0) for t in range(3)]

    # logits = h·W2 + b2
    dW2 = [[0.0] * 3 for _ in range(2)]
    db2 = [dlogits[t] for t in range(3)]
    dh = [0.0, 0.0]
    for t in range(3):
        for j in range(2):
            dW2[j][t] = dlogits[t] * h[j]
            dh[j] += dlogits[t] * W2[j][t]

    # tanh:  dpre[j] = dh[j] * (1 - h[j]^2)
    dpre = [dh[j] * (1 - h[j] ** 2) for j in range(2)]

    # pre = flat·W1 + b1
    dW1 = [[0.0] * 2 for _ in range(6)]
    db1 = [dpre[j] for j in range(2)]
    dflat = [0.0] * 6
    for j in range(2):
        for k in range(6):
            dW1[k][j] = dpre[j] * flat[k]
            dflat[k] += dpre[j] * W1[k][j]

    # flat 来自 emb 展平，emb 来自 C[X]
    dC = [[0.0, 0.0] for _ in range(3)]
    for i in range(3):
        ch = X[i]
        dC[ch][0] += dflat[i * 2 + 0]
        dC[ch][1] += dflat[i * 2 + 1]

    return dC, dW1, db1, dW2, db2, dprobs, dlogits, dh, dpre, dflat


dC, dW1, db1, dW2, db2, dprobs, dlogits, dh, dpre, dflat = backward(
    flat, pre, h, probs
)

print()
print("=" * 60)
print("BACKWARD（反向）")
print("=" * 60)
print(f"dprobs = {[f'{v:.6f}' for v in dprobs]}")
print(f"dlogits = {[f'{v:.6f}' for v in dlogits]}")
print(f"dh = {[f'{v:.6f}' for v in dh]}")
print(f"dpre = {[f'{v:.6f}' for v in dpre]}")
print(f"dflat = {[f'{v:.6f}' for v in dflat]}")
print()
print("dC (3x2):")
for i, row in enumerate(dC):
    print(f"  dC[{i}] = {[f'{v:.6f}' for v in row]}")
print("dW1 (6x2):")
for i, row in enumerate(dW1):
    print(f"  dW1[{i}] = {[f'{v:.6f}' for v in row]}")
print(f"db1 = {[f'{v:.6f}' for v in db1]}")
print("dW2 (2x3):")
for i, row in enumerate(dW2):
    print(f"  dW2[{i}] = {[f'{v:.6f}' for v in row]}")
print(f"db2 = {[f'{v:.6f}' for v in db2]}")


# ---------------- 数值微分验证 ----------------
print()
print("=" * 60)
print("数值微分验证（finite differences）")
print("=" * 60)


def loss_from(C_, W1_, b1_, W2_, b2_):
    emb = [C_[x][:] for x in X]
    flat = [v for row in emb for v in row]
    pre = [b1_[j] + sum(flat[k] * W1_[k][j] for k in range(6)) for j in range(2)]
    h = [math.tanh(p) for p in pre]
    logits = [b2_[t] + sum(h[j] * W2_[j][t] for j in range(2)) for t in range(3)]
    counts = [math.exp(l) for l in logits]
    z = sum(counts)
    probs = [c / z for c in counts]
    return -math.log(probs[Y])


def numeric_grad(f, eps=1e-5):
    import copy
    def wrap(name):
        base = f()
        return name
    # 对每个参数逐元素做中心差分
    results = []

    def check(name, get, set_):
        base_val = None
        # 先对 get 返回的整个参数做拷贝
        pass

    # C
    L0 = loss_from(C, W1, b1, W2, b2)
    for name, param, shape in [
        ("C", C, (3, 2)), ("W1", W1, (6, 2)), ("b1", b1, (2,)),
        ("W2", W2, (2, 3)), ("b2", b2, (3,)),
    ]:
        # 深拷贝参数
        import copy
        P = copy.deepcopy(param)
        grads = copy.deepcopy(param)
        def set_all(P):
            pass
        # 展开索引
        idxs = []
        if len(shape) == 1:
            idxs = [(i,) for i in range(shape[0])]
        else:
            idxs = [(i, j) for i in range(shape[0]) for j in range(shape[1])]
        for idx in idxs:
            def make_params(delta):
                P2 = copy.deepcopy(P)
                if len(idx) == 1:
                    P2[idx[0]] += delta
                else:
                    P2[idx[0]][idx[1]] += delta
                if name == "C":
                    args = (P2, W1, b1, W2, b2)
                elif name == "W1":
                    args = (C, P2, b1, W2, b2)
                elif name == "b1":
                    args = (C, W1, P2, W2, b2)
                elif name == "W2":
                    args = (C, W1, b1, P2, b2)
                else:
                    args = (C, W1, b1, W2, P2)
                return loss_from(*args)
            lp = make_params(eps)
            lm = make_params(-eps)
            g = (lp - lm) / (2 * eps)
            if len(idx) == 1:
                grads[idx[0]] = g
            else:
                grads[idx[0]][idx[1]] = g
        results.append((name, grads))

    return results


num_grads = numeric_grad(loss_from)
analytical = {"C": dC, "W1": dW1, "b1": db1, "W2": dW2, "b2": db2}

def flatlist(v):
    if isinstance(v[0], list):
        return [x for row in v for x in row]
    return list(v)

all_ok = True
for name, g in num_grads:
    an = flatlist(analytical[name])
    nu = flatlist(g)
    err = max(abs(a - b) for a, b in zip(an, nu))
    ok = err < 1e-4
    all_ok &= ok
    print(f"{name:>3}: 解析梯度 vs 数值梯度 最大误差 = {err:.2e}  {'OK' if ok else 'FAIL'}")
print()
print("结论:", "全部匹配，手算梯度正确 [OK]" if all_ok else "有偏差，需检查 [FAIL]")
