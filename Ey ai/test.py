'''
 llm_url="http://localhost:8080/chat/completions"
token_url="http://localhost:8080/generate_tokens"
client_secret="ajkd2BKDJKALDFABKSAcdgbabn"
model_name= "gpt-oss-20b"
RPM= 20 request per minute
client.generate("What is the addition of two and three divided by 10")
 
1. Implement a client class that has generate public method and should always return string as output.
2. You should implement a method to get access token, use this access token to call the model as authorization.
3. You should also take care of request per minute. If request fails implement retry .
4. Use Python Request module to make http requests for getting access token and also for calling the llm.

'''

llm_url="http://localhost:8080/chat/completions"
token_url="http://localhost:8080/generate_tokens"
client_secret="ajkd2BKDJKALDFABKSAcdgbabn"
model_name= "gpt-oss-20b"
RPM= 20 #request per minute


import requests

class Client:
    
    request_count = 0
    
    def __init__(self):
        pass
    
    def generate(self, query): #->str
    
        url = llm_url
        access_token = get_access_token(client_secret)
        
       params = {
           "query": query,
           "model_name": model_name,
           "client_secret": access_token,
           
       }
       
       llm_response = requests.post(url, params)
       
       retrun llm_response.body()
        # implement retry 
       
   
    
    def get_access_token(client_secret):
       url = token_url
       
       params = {
           "client_secret": access_token,
           
       }
       
       request_count ++
       
       if(request_count > RPM):
            #   delay
            self.get_access_token()
       try:
            response = requests.post(url, params)
            return response
        except(e):
            print
            
    # implement retry   
    

client = Client()
client.generate("What is the addition of two and three divided by 10")
   

    

