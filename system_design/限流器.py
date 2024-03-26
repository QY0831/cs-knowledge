"""
创建一个中间件，作为限流器，限制客户端对API服务器的请求。
- 可以使用云微服务部署

令牌桶算法（Token Bucket）
桶大小：桶内最多允许多少个代币
令牌按照速率放入桶，一旦桶满，就不再加入令牌。
每次请求消耗一个代币：
 - 请求达到时，取出一个代币，请求通过
 - 没有足够代币，请求丢弃
通常，不同的API端点需要不同的桶。
"""

import time

class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity = capacity  # 令牌桶的容量
        self.rate = rate  # 令牌生成速率（单位：令牌/秒）
        self.tokens = capacity  # 当前令牌数量
        self.last_refill_time = time.time()  # 上次令牌生成时间

    def _refill_tokens(self):
        now = time.time()
        elapsed_time = now - self.last_refill_time
        new_tokens = elapsed_time * self.rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill_time = now

    def consume(self, num_tokens):
        if num_tokens <= self.tokens:
            self.tokens -= num_tokens
            return True
        else:
            self._refill_tokens()
            if num_tokens <= self.tokens:
                self.tokens -= num_tokens
                return True
            else:
                return False


# 创建一个容量为10，速率为2的令牌桶
bucket = TokenBucket(10, 2)

# 模拟处理10个请求
for i in range(1, 11):
    if bucket.consume(1):
        print(f"Request {i}: Allowed")
    else:
        print(f"Request {i}: Denied")
    time.sleep(0.5)

