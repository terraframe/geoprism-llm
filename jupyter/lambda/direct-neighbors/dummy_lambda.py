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
def execute(names: List[str]) -> str:
    conn = Neo4jConnection(uri=os.getenv('NEO4J_URI'), user=os.getenv('NEO4J_USERNAME'), pwd=os.getenv('NEO4J_PASSWORD'))
    
    try:
        result = ""
        
        for name in names:        
        
            """
            Collects the neighborhood of entities mentioned
            in the question
            """
            response = conn.query(
                """CALL db.index.fulltext.queryNodes('entities', $query, {limit:5})
                YIELD node,score
                CALL (node, node){
                    WITH node
                    MATCH (node)-[r]->(neighbor)
                    RETURN LABELS(node)[1] + ' ' + node.name + ' - ' + type(r) + ' -> ' + neighbor.name AS output
                    UNION ALL
                    WITH node
                    MATCH (node)<-[r]-(neighbor)
                    RETURN LABELS(neighbor)[1] + ' ' + neighbor.name + ' - ' + type(r) + ' -> ' + node.name AS output
                }
                RETURN output LIMIT 15
                """,
                {"query": name},
            )
            result += "\n".join([el['output'] for el in response]) 
            
        return result        
    finally:
        conn.close()


def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
    
    locations = execute(parameters[0]["value"])

    responseBody =  {
        "TEXT": {
            "body": locations
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
