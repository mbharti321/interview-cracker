arr = [3,4,9,10,6,23] # -> 16 -> return index of pair which adds up to K
k = 16
# previous = arr[0]

def my_fun(arr, k):
    for i in range(len(arr) - 1):
        if(k - arr[i] == arr[i+1]):
            return((i, i+1))
    
    return []

print(my_fun(arr, k))
    

            
            

            
