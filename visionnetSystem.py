my_str = '(()()()(()())' # false
# my_str = '()()()(()())' # true

def check_valid_paran(my_str):
    stack = []
    
    for ch in my_str:
        if(ch == '('):
            stack.append('(')
        else:
            if(len(stack) ==0):
                return False
            stack.pop()
        
    if(len(stack) != 0):
        return False
    
    return True
    
print(check_valid_paran(my_str))
    