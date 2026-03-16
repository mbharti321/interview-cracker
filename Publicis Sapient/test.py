'''
- RAG project explanation
- Agentic AI project explanation
- what are tools
- How did i use service bus and event hub in projects
- How did we evaluate the performance of the model in RAG project, metrics
- How did we reduce halucination in RAG project
- What embedding model did we use in RAG project and why
1. write a decorator to calculate the time taken by a function to execute

# 2. whats MRO
    class A: pass

    class B(A): pass

    class C(A): pass
    # class C(A): pass

    class D(B,C): pass #multiple inheritance allowed or not?

    print(D.mro())
'''


# 1. write a decorator to calculate the time taken by a function to execute

import time

def my_decorator(func):
    def wrapper(*args, **arws):
        # before
        # print(**arws)
        t1 = time.time()
        # print(type(arws))
        
        func(arws["num"])
        
        t2 = time.time()
        # after
        print(t2-t1)
    
    return wrapper


@my_decorator
def count(num=10):
    for i in range(1,num):
        print(i)
 
count(num=10)


# ----
# 2. whats MRO
class A: pass

class B(A): pass

class C(A): pass
# class C(A): pass

class D(B,C): pass #multiple inheritance allowed or not?

print(D.mro())
# MRO
# D -> B -> C -> A
# D -> B -> A -> C