"""
装饰器模式：
在不改变原有实现的前提下，给一个对象增加新的功能。

比统计方法执行时间。
"""
import time

def calculate_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"方法 {func.__name__} 的执行时间为：{execution_time} 秒")
        return result
    return wrapper


@calculate_execution_time
def my_method():
    # 需要统计执行时间的方法代码
    time.sleep(2)

my_method()