''''
pdf with different type of data text , image, table, graph, etc. unstructured data like patient records, receipts, etc.

Generate a solution to extract the data from the pdf  -> use it for different use cases -> RAG -> call SQL database for relevent data
validate guidelines, different check list for insaurence company
Hospital will be uploading patients documents, the solution will tell whether patient is eligible for the insurance or not based on the check list provided by the insurance company.
    -> the solution will be extracting the data from the documents 
    -> validate the data with the check list from sql database
    -> response to the hospital whether the patient is eligible for the insurance or not
    
if RAG is valid solution for this use case or not? Why?
Optimal solution for this use case 
'''


# get the square of even numbers from the list
arr = [1,2,3,4,5]

# output -> square of evens -> [4, 16]

result = [num * num for num in arr if num%2 ==0]
print(result)


'''
create 2 lists [1,2,3] [4,5,6]  
output: [(1,4),(2,5),(3,6)]
'''

arr1 =  [1,2,3] 
arr2 = [4,5,6]  
result1 = []
for i,j in zip(arr1, arr2):
    result1.append((i,j))
    
print(result1)