# arr = [-2,1,-3,4,-1,2,1,-5,4] # output = [4,-1,2,1]
# # arr= [5,4,-1,7,8] #Output: [5,4,-1,7,8]
# # input = [8,-19,5,-4,20] #Output : [5,-4,20]
# # max_sub_arr

# arr = [-1]

# max_sum = -9999999999999999999999
# max_sub = arr
# start = 0
# end = len(arr) - 1

# start_updated = False
# while(start<end):
#     cur_sum = sum(arr[start:end+1]) 
    
#     if(cur_sum > max_sum):
#         max_sum = cur_sum
#         max_sub = arr[start:end+1]
    
#     if(start_updated):
#         end -= 1
#     else:
#         start += 1
        
        
# print(max_sum)
# print(max_sub)

# nums = [i^2 for i in range(10)]
# print(nums)
# '''
# Input : [[Rahul], [divya], [karan], [manish], [satish]]
 
# Output : [Rahul, divya, karan, manish, satish]
# '''
# arr = [["Rahul"], ["divya"], ["karan"], ["manish"], ["satish"]]
# result = [name for sub in arr for name in sub]

# print(result)


# arr = ['Rahul', 'divya', 'karan', 'manish', 'satish']

# def generate_name():
#     for name in arr:
#         yield name
        
# # print(next(generate_name))
# print(generate_name().next())

# async function
def fuc2():
    # calcun

def asyc my_func():
    # cpu operation
    db_result = await call_db() # 4sec  -> coroutine -> wait for respone
    # other cpu tasks
    #  response came from call_db() -> gets 
    
    


 
    






