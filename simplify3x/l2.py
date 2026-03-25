'''
explain LLM to 15yo

explain it to software engineer with understanding of machine learning
whats rag
guardrails, types of guardrails
Whats prompt engineering, types of prompt engineering
diff between system, user, dev prompts
how to evaluate gen ai agent, what are the metrics, how to do it in production
whats chunking
whats overlap chunking?
how to handle hallucination in gen ai agent?
prompt injection attack, how to handle it?

py
generator
decorator how to implement it

'''




a= [[1,2,3], [4,5,6]]
# out [1,2,3,4,5,6]

# result = [i for el in a for i in el]
# result2 = [i for el in a for i in el if i%2 == 0]

# print(result)
# print(result2)

import time

def my_decorator(func):
    def wrapper(*arg, **kawr):
        t1 = time.time()
        func(*arg)
        t2 = time.time()
        
        print(t2-t1)
        
    return wrapper
        

@my_decorator
def filter(a):
    result = [i for el in a for i in el]
    result2 = [i for el in a for i in el if i%2 == 0]
    
    print(result)
    print(result2)
    
filter(a)