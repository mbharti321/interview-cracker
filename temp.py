# 3rd highest salary without using limit and off

# select salary, 
# 	Rank(order by salary desc) as rk
# from employee where rk = 3

# 1 employee -> manageerid + empId + salary
# -> employees whose salry is gt manager's salary

# select 
# 	employee.name
# from employee emp
# 	join employee mg on mg.empid == emp.managerId
# where emp.salary > mg.salary


# st = "I am a Engineer"
# out = "Engineer a am I?"

st = "I am a Engineer"
words = st.split(" ")
# print(words)
out = ""
for i in range(len(words)-1, -1, -1):
    # print(i, words[i] )
    out = out + words[i] + " "
 
out = out + "?"
 
print(out)


di1 = {'Jock':['32','Male'],'Joe':['32','Male'],'Jofh':'22','j':['32','Male']}

di2 = {}
for (key,value) in di1.items():
    # print(type(value))
    if type(value) == list:
        di2[key] = value
        
print(di2)


# Sort the list below list without build in function.
# nums=[5,4,2,8,7,6,9]

nums=[5,4,2,8,7,6,9]

for i in range(len(nums)):
    for j in range(0, len(nums)-1-i):
        if(nums[j] > nums[j+1]):
            nums[j], nums[j+1] = nums[j+1], nums[j]

print(nums)
    