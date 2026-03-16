# list -> retun duplicete elements

arr = [1,2,4,5,3,2,1]

seen = set()

result = []
for el in arr:
    if(el in seen):
        result.append(el)
    else:
        seen.add(el)
        
print(result)



# // Palindrom
# using System;

# public class HelloWorld
# {
#     public static void Main(string[] args)
#     {
#         Console.WriteLine ("Try programiz.pro");
#         string myStr = "hellolleh";
#         bool isPalindrom = checkPalindrom(myStr);
#     }
    
#     public static bool checkPalindrom(string str)
#     {
#         int start = 0;
#         int end = 
        
#     }
    
    
# }