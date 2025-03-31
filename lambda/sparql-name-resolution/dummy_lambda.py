import requests
import json


# Fulltext index query
def execute(name: str) -> str:
    
    statement = (
        f"PREFIX   ex: <https://localhost:4200/lpg/graph_801104/0/rdfs#>\n" 
        f"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
        f"PREFIX text: <http://jena.apache.org/text#>\n"
        f"PREFIX lpgs: <https://localhost:4200/lpg/rdfs#>\n"
        
        f"SELECT ?code ?type\n"
        f"FROM <https://localhost:4200/lpg/graph_801104/0#>\n"
        f"WHERE {{\n"
        f"	?s text:query (rdfs:label '{name}') .\n"
        f"	?s lpgs:GeoObject-code ?code .\n"
        f"	?s a ?type .\n"
        f"}}\n"
    )
    
    response = requests.post('http://ec2-52-24-108-177.us-west-2.compute.amazonaws.com:3030/flood/', data={'query': statement})
    
    responseJson = response.json()
    
    results = []
    
    for r in responseJson.get('results').get('bindings'):
        data = {}
        data['code'] = r.get('code').get('value')
        data['type'] = r.get('type').get('value')        
        results.append(data)

    return results    

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
    
    result = execute(parameters[0]["value"])

    responseBody =  {
        "TEXT": {
            "body": json.dumps(result)
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
