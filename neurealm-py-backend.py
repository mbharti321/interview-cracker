# 23 feb

# create a factory pattern for insaurence
'''
insaurence -> health, life, term....

'''

class Insurance:
    amount = 0
    def __init__(self, amount):
        self.amount = amount

class HealthInsurance(Insurance):
    amount = 0
    def __init__(self, amount):
        super().__init__(amount)

class TermInsurance(Insurance):
    amount = 0
    def __init__(self, amount):
        super().__init__(amount)
        
class LifeInsurance(Insurance):
    amount = 0
    def __init__(self, amount):
        super().__init__(amount)

class InsuranceFactory:
    def CreateInsurance(self, insuranceType):
        if(insuranceType == "health"):
            return  HealthInsurance
        elif(insuranceType == "term"):
            return  TermInsurance
        elif(insuranceType == "life"):
            return  LifeInsurance
        else:
            return None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
list = [1,0,2,3,0,0,4]
output = [1,2,3,4,0,0,0]

start
end
loop:
    # zeroQueue=[]
    
    if(0):
        save index of 0,
    
    if(non 0):
        get oldest

'''

# decorator

def my_decorator(func):
    # def wrapper(func):
    def wrapper(*args, **arws ):
        print("before......")
        func()
        print("after......")
        
    return wrapper

@my_decorator
def myFun():
    print("hello")
    

myFun()   
