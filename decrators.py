
# function based decrator__________________

def decrator(decrated_function):
    def wrapper_fun(*args, **kwargs):
        print(f"decrator excut thi befor {decrated_function.__name__}")
        decrated_function(*args, **kwargs)
        print("after decrated_fun")
    return wrapper_fun

@decrator
def decrated_function(name, age):
    print(f"my name is {name}")
    print(f"my age is {age}")

# decrated_function("ziya", 32)

# class based decrator__________________

class decrator():
    def __init__(self, decrated_function):
        self.decrated_function = decrated_function

    def __call__ (self,*args, **kwargs):
        print(f"decrator excut thi befor {self.decrated_function.__name__}")
        print("after decrated_fun")
        pp = self.decrated_function(*args, **kwargs)
        return pp

@decrator
class decrated_function():
    def __init__(self, name, age):
        print(f"my name is {name}")
        print(f"my age is {age}")
        self.name = name
        self.age = age
    def see_togather(self):
        print(f"my name is {self.name}, my age is {self.age}")


# pp = decrated_function("ziya", 32)
# pp.see_togather()

# decrate class with function __________________

def decrator(fun):
    def wraper(*args, **kwargs):
        print(f"decrator excut thi befor {fun.__name__}")
        print("after decrated_fun")
        gg =fun(*args, **kwargs)
        return gg
    return wraper

@decrator
class decrated_function():
    def __init__(self, name, age):
        print(f"my name is {name}")
        print(f"my age is {age}")
        self.name = name
        self.age = age
    def see_togather(self):
        print(f"my name is {self.name}, my age is {self.age}")


pp = decrated_function("ziya", 32)
pp.see_togather()


# decrate function with class __________________


class decrator():
    def __init__(self,fun):
        self.fun = fun
        print(f"decrator excut thi befor {self.fun.__name__}")
        print("after decrated_fun")

    def __call__(self, *args, **kwds):
        print("hello")
        self.fun(*args, **kwds)
        print("after hello") 


@decrator
def decrated_function(name, age):
        print(f"my name is {name}")
        print(f"my age is {age}")
        print(6+8)
        print(f"my name is {name}, my age is {age}")

decrated_function("ziya", 32)