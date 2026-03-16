# string -> find most repeated char

string = "hello worjlhgvcbjdddddf"

ch_dict = {}

most_repeated = [string[0],1]

for ch in string:
    if ch in ch_dict:
            
        ch_dict[ch] = ch_dict[ch] +1
        
        if(ch_dict[ch] +1 > most_repeated[1]):
            most_repeated = [ch, ch_dict[ch] ]
    else:
        ch_dict[ch] = 1


print(most_repeated)



from fastapi import FastAPI

app =  FastAPI()


@app.get("/greet/{id}")
def greet(id: int):
    return "Hello World!"
    
@app.post("/greet")
def greet(user: User):
    return "Hello World!"
    
    

uvicorn main:app --reload


user -
employee

list custormers with no orders

customer table -> id, name
--
order table -> orderid, cust_id, date

select customerName, 
    count(cust_id) as count
from customers c
left join orders o on c.cust_id == o.cust_id
    group by cust_id
having count(cust_id)  == 0


