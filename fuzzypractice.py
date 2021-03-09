from fuzzywuzzy import fuzz
from fuzzywuzzy import process

validoptions = ["pizza","menu","order","exit","ice cream","soup"]


choices = []
exit = False
while True:
    query = input(f'{" or ".join(validoptions)}? ')
    
    (match, confidence) = process.extractOne(query, validoptions)
    
    print(f"{query}:  mathces: {match} at {confidence}%")
    