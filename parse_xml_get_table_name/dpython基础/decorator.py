# 1. 装饰器（带参 / 不带参）
# 装饰器作用
# 本质是函数，用来包装其他函数，增强或改变被装饰函数行为。

# 常用于日志记录、权限校验、性能监控等。

from functools import wraps

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def log_decorator2(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数 {func.__name__}，参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"函数 {func.__name__} 返回: {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

add(3, 4)


def repeat(num_times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            for _ in range(num_times):
                print(f"第 {_+1} 次调用")
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
