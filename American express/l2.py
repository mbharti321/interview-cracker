
''''
- whats rag, why rag needed, why not just call llm, how to implement it
- multi agent system project
- why multi agent required, why not signle agent doing all the work?
- what debugging challanges we can face in single agent system
- how to evaluate your gen ai agent, what are the metrics, how to do it in production
- guardrails
- what safety machenisms we can implement in gne ai system, how to implement it
- how to avoid hallucination in gen ai system, how to handle it if it happens
- how to handle prompt injection attack, how to avoid it, how to handle it if it happens
    - we can use guardrails to handle it
    - what if guardrails also get bypassed, how to handle it, how to detect it, how to recover from it
- 

'''





# program to check if a meeting can be booked given the existing meetings in a day
existing_meetings = [(9, 10), (12, 13), (15, 16)] 

#  check if the the meeting can be booked 
can_book(existing_meetings, (10, 12)) # True 
can_book(existing_meetings, (11, 12)) # True 
can_book(existing_meetings, (9, 11)) # False 
can_book(existing_meetings, (13, 15)) # True 
can_book(existing_meetings, (14, 16)) # False

'''

'''
def can_book(existing_meetings, (10, 12)):
    '''
        occupied_hours: set ("9-10", "15-16", "16-17", "17-18") # split the existing meetings into a set of occupied hours 
            -> 10-12 -> true, available # split new meeting into hours and check if any of them are occupied, return false 
                - 10-11 -> false
                - 11-12 -> false
            -> 9-11  -> false, not available
                - 9-10 -> true
                - 10-11 -> false
    '''
    
    
    
    
    pass