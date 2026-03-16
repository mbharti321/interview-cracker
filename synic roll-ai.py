"""
Scenario: You are building a Python-based RAG tool for Client to process a "Brewery Operations Manual" for an AI Agent. Before text is embedded, it must be segmented into chunks of 500 characters with a 50-character overlap to preserve context at boundaries.
Task: Write a Python function get_chunks(manual_text, chunk_size, overlap) that returns a list of text segments where each new chunk starts with the last 50 characters of the previous chunk.

"""
def get_chunks(manual_text, chunk_size, overlap):
    
    result_list = []
    # 2000 -> 250 -> 200 -> 
    # 200, 50 -> 250
    
    while(len(manual_text) > chunk_size):
        result_list.append(manual_text[0:chunk_size+overlap])
        # reduce the manual text
        manual_text = manual_text[chunk_size:]
        
    result_list.append(manual_text)
    
    return result_list
    
data = '''Scenario: You are building a Python-based RAG tool for Client to process a "Brewery Operations Manual" for an AI Agent. Before text is embedded, it must be segmented into chunks of 500 characters with a 50-character overlap to preserve context at boundaries.
Task: Write a Python function get_chunks(manual_text, chunk_size, overlap) that returns a list of text segments where each new chunk starts with the last 50 characters of the previous chunk.Scenario: You are building a Python-based RAG tool for Client to process a "Brewery Operations Manual" for an AI Agent. Before text is embedded, it must be segmented into chunks of 500 characters with a 50-character overlap to preserve context at boundaries.
Task: Write a Python function get_chunks(manual_text, chunk_size, overlap) that returns a list of text segments where each new chunk starts with the last 50 characters of the previous chunk.
Scenario: You are building a Python-based RAG tool for Client to process a "Brewery Operations Manual" for an AI Agent. Before text is embedded, it must be segmented into chunks of 500 characters with a 50-character overlap to preserve context at boundaries.
Task: Write a Python function get_chunks(manual_text, chunk_size, overlap) that returns a list of text segments where each new chunk starts with the last 50 characters of the previous chunk.'''
chunk_size = 200
overlap = 10
result = get_chunks(data, chunk_size, overlap)
for i in result:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(i)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")