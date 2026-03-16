

def my_decorator(func):
    def wrapper(*args, **arws):
        print("Hi")
        func(args[0])
        print("Good morning!")
        print(args)
        print(arws)
    
    return wrapper


# hi
# Manish
# Good morning
# ["Manish", "hello", 1,3]
# {count:2}

@my_decorator
def greet(name, *args, **arws):
    print(name)
    
greet("Manish", "hello", 1,3, count=2)
    # my_decorator("hello", 1,3, count:2)
    
    
# list -> [3,4,9,10,23]
# 16

    