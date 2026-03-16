nums = [1,0,0,1,1,0,0]
# [1,1,1,0,0,0,0]

start = 0
end = len(nums)-1

while(start<end ):
    if(nums[start] == 1):
        start +=1
    if(nums[end] == 0):
        end -=1
    if((nums[start] != 1) and (nums[end] != 0)):
        nums[start], nums[end] = nums[end], nums
    
    print(start, end)

print(nums)

# zero_count = 0
# one_count = 0

# for num in nums:
#     if(num == 0):
#         zero_count +=1
#     else:
#         one_count +=1

# result = []
# for i in range(one_count):
#     result.append(1)
    
# for i in range(zero_count):
#     result.append(0)
    
# print(result)