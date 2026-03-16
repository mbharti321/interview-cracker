a = [1,2,3]
b = a
c = a[:]

print(a is b) # true
print(a is c) # False


g = (i for i in range(3)) # 012
list(g) # [0,1,2]
list(g) # [0,1,2]


# fastapi api creation
from fastapi import FastAPI

app = FastAPI()


# define 
@app.get('/')
def my_fun():
    return "hello"