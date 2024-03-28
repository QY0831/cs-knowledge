"""
推特snowflake算法:
分布式系统中的唯一ID生成器
"""
import time

class Snowflake:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1

    def generate_id(self):
        timestamp = int(time.time() * 1000)

        if timestamp < self.last_timestamp:
            raise Exception("Invalid system clock")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 4095 # 4095 = 0b111111111111
            if self.sequence == 0:  # 该timestamp的sequence用完，需要等待timestamp更新
                timestamp = self.wait_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # 生成Snowflake ID
        snowflake_id = ((timestamp - 1546300800000) << 22) | (self.machine_id << 12) | self.sequence
        return snowflake_id

    def wait_next_millis(self, last_timestamp):
        timestamp = int(time.time() * 1000)
        while timestamp <= last_timestamp:
            timestamp = int(time.time() * 1000)
        return timestamp

# 示例用法
snowflake = Snowflake(machine_id=1)
unique_id = snowflake.generate_id()
print(unique_id)
