# output of below program
funcs = []

for i in range(3):
 funcs.append(lambda: i) #
 
print([f() for f in funcs]) #-> [2,2,2]


# output of below program
def add_item(item, items=[]):
    items.append(item)
    return items
    
print(add_item("apple"))
print(add_item("banana"))
print(add_item("orange"))

# [apple]
# [banana]
# [orange]


