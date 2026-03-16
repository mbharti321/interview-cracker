from fastapi import FastAPI, File
from typing import Annotated

'''
input log
api to accept log file -> 
    - count errors, infos
    - print the output



"2026-02-23 10:15:30 ERROR Payment failed"
"2026-02-23 10:16:02 INFO User logged in"
"2026-02-23 10:17:45 ERROR Timeout occurred"

'''


app = FastAPI()

@app.get('/')
def greet():
    return "hello"

@app.post('/check_logs')
def process_log_file(log_file: Annotated[bytes, File()]):
    # return  len(log_file)
    # print("fileName", log_file.filename)
    
    log_file_content = log_file.decode('utf-8').splitlines()
    # print()
    print(log_file_content)
    
    result = {
        "error": 0,
        "info": 0
    }
    # loop through lines
    for line in log_file_content:
        print(line)
        
        if("ERROR" in line):
            result["error"] += 1
    
        if("INFO" in line):
            result["info"] += 1
    
    
    return result
    