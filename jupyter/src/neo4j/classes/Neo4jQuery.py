
import os
from dotenv import load_dotenv 
from typing import List
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
from langchain_core.documents import Document
from classes import Neo4jConnection

load_dotenv() 

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
def execute_cypher(cypher: str) -> str:
    conn = Neo4jConnection(uri=os.getenv('NEO4J_URI'), user=os.getenv('NEO4J_USERNAME'), pwd=os.getenv('NEO4J_PASSWORD'))
    
    try:
        
        response = conn.query(cypher, {})
        result = "\n".join([el['output'] for el in response])
        
        return result        
    finally:
        conn.close()


# Fulltext index query
def most_likely_name(name: str) -> str:
    conn = Neo4jConnection(uri=os.getenv('NEO4J_URI'), user=os.getenv('NEO4J_USERNAME'), pwd=os.getenv('NEO4J_PASSWORD'))
    
    try:
        
        """
        Collects the neighborhood of entities mentioned
        in the question
        """
        response = conn.query(
            """
            CALL db.index.fulltext.queryNodes('entities', $query, {limit:5})
            YIELD node,score
            RETURN node.code AS code LIMIT 1
            """,
            {"query": generate_full_text_query(name)},
        )
        return response[0]['code'];
    finally:
        conn.close()


# Fulltext index query
def basic(names: List[str]) -> List[Document]:
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
            
        return [Document(page_content=result)]        
    finally:
        conn.close()
        
# Fulltext index query
def formatted(names: List[str]) -> List[Document]:
    conn = Neo4jConnection(uri=os.getenv('NEO4J_URI'), user=os.getenv('NEO4J_USERNAME'), pwd=os.getenv('NEO4J_PASSWORD'))
    
    try:        
        groups = {}
        items = {}
        edges = {}
        documents = []
        
        for name in names:                
            response = conn.query(
                """CALL db.index.fulltext.queryNodes('entities', $query, {limit:5})
                YIELD node,score
                CALL (node, node){
                    WITH node
                    MATCH (node)-[r]->(neighbor)
                    RETURN node AS target, type(r) AS edge, neighbor AS source
                    UNION ALL
                    WITH node
                    MATCH (node)<-[r]-(neighbor)
                    RETURN neighbor AS target, type(r) AS edge, node AS source
                }
                RETURN source, edge, target LIMIT 15
                """,
                {"query": generate_full_text_query(name)},
            )
        
            for row in response:
            
                record = row.data()
            
                key = record['source']['code']
            
                items[key] = record['source']
                items[record['target']['code']] = record['target']
                edges[key] = record['edge']
            
                if key not in groups:
                    groups[key] = []

                groups[key].append(record['target']['code'])
                                
        for key in groups:
            sourceName = items[key]['name']
            edgeName = edges[key]
            
            if edgeName == 'HAS_SCHOOL_ZONE':           
                content = 'The following schools are part of ' + sourceName + ': ' + (', '.join(map(lambda x: items[x]['name'], groups[key] ))) + '.'
            else:
                content = 'The following schools are in the flood area ' + sourceName + ': ' + (', '.join(map(lambda x: items[x]['name'], groups[key] )))
                        
            documents.append(Document(page_content=content))

        return documents
    finally:
        conn.close()
