class Foo:
    def __hash__(self): return 1
    def __eq__(self, other): return True

a = Foo()
b = Foo()

print(a == b)        # True，调用了 __eq__
print(hash(a))       # 1，调用了 __hash__
print({a, b})        # 只会存一个，认为两个对象相等且哈希相同
