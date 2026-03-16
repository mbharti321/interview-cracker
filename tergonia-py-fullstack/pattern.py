
def some_function(n):

    for i in range(1, n + 1): # 1,2, 3,4, 5
        print(" " * (n - i) + "*" * (2 * i - 1)) 


    for i in range(n - 1, 0, -1): # 4, 3, 2, 1 ->
        print(" " * (n - i) + "*" * (2 * i - 1))

some_function(5)
'''
_ _ _ _ *

_ _ _ * * *

_ _ * * * * *

_ * * * * * * *

* * * * * * * * *



_ * * * * * * *

_ _ * * * *
_ _ _ * * 
_ _ _  *

'''