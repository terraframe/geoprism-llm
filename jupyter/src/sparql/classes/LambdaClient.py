
import os
from dotenv import load_dotenv 
from typing import List
from langchain_core.documents import Document
import requests

# The API endpoint

load_dotenv() 

# Fulltext index query
def lambda_basic(names: List[str]) -> List[Document]:
    result = ""
        
    for name in names:                
        response = requests.get(os.getenv('LAMBDA_URI'), params={'names': name})
        
        response_json = response.json()
        
        result += response_json['content'] + "\n"    
            
    return [Document(page_content=result)]        
        
