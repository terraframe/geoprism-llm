import json

from typing import List
from neo4j import GraphDatabase
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
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

def generate_full_text_query(input: any) -> str:
    """
    Generate a full-text search query for a given input string.

    This function constructs a query string suitable for a full-text search.
    It processes the input string by splitting it into words and appending a
    similarity threshold (~2 changed characters) to each word, then combines
    them using the AND operator. Useful for mapping entities from user questions
    to database values, and allows for some misspelings.
    """
    
    full_text_query = ""
    words = [el for el in remove_lucene_chars(input).split() if el]
    for word in words[:-1]:
        full_text_query += f" {word}~2 AND"
    full_text_query += f" {words[-1]}~2"
    
    return full_text_query.strip()


# Fulltext index query
def basic(names: List[str]) -> str:
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
                {"query": generate_full_text_query(name)},
            )
            result += "\n".join([el['output'] for el in response]) 
            
        return result        
    finally:
        conn.close()


def lambda_handler(event, context):
    if 'names' in event:
            
        content = basic(event['names'])

        return {
            'statusCode': 200,
            'body': json.dumps({'content':str(content)})
        }        
    elif 'queryStringParameters' in event:
        req = event.get("queryStringParameters", None)
        name = req.get("names", "").strip()
        
        if name == "":
            return {
                'statusCode': 400,
                'body': json.dumps({'error':'Missing names parameter'})
            }

        content = basic(name.split(","))

        return {
            'statusCode': 200,
            'body': json.dumps({'content': str(content)})
        }                    
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error':'Missing names parameter'})
        }

