# 预处理
# 埃氏筛
MX = 10 ** 6 + 10
primes = []
is_prime = [True] * MX
is_prime[1] = False
for i in range(2, MX):
    if is_prime[i]:
        primes.append(i)
        for j in range(i * i, MX, i):
            is_prime[j] = False

# 直接判断
def is_prime(n: int) -> bool:
    return all(n % i for i in range(2, isqrt(n) + 1))
