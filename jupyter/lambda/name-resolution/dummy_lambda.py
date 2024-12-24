import json

from typing import List
from neo4j import GraphDatabase
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response


# Fulltext index query
def execute(name: str) -> str:
    conn = Neo4jConnection(uri=os.getenv('NEO4J_URI'), user=os.getenv('NEO4J_USERNAME'), pwd=os.getenv('NEO4J_PASSWORD'))
    
    try:
       
        response = conn.query(                
            """
            CALL db.index.fulltext.queryNodes('entities', $query, {limit:5})
            YIELD node,score
            RETURN node.code AS code LIMIT 1
            """,
            {"query": name})
            
        return response[0]['code']            
    finally:
        conn.close()


def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    result = execute(parameters[0]["value"])

    responseBody =  {
        "TEXT": {
            "body": str(result)
        }
    }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }

    }

    dummy_function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(dummy_function_response))

    return dummy_function_response
