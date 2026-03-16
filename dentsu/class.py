# output of below program
class BaseModel:
    @staticmethod
    def process(self):
        return self.step1() + self.step2()
        
    def step1(self):
        return "base1"
    def step2(self):
        return "base2"
 
class CustomModel(BaseModel):
    def step2(self):
        return "custom2"   
        
        
m = CustomModel()
print(m.process()) #-> "base1custom2"