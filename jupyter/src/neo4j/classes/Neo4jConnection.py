from neo4j import GraphDatabase

class Neo4jConnection:
    
    def __init__(self, driver):
        self.__driver = driver
    
        
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
    
    @classmethod
    def with_user(cls, uri, user, pwd):
        try:
            return cls(GraphDatabase.driver(uri, auth=(user, pwd)))
        except Exception as e:
            print("Failed to create the driver:", e)