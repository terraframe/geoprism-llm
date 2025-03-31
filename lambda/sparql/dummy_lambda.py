import requests


# Fulltext index query
def execute(statement: str) -> str:
    response = requests.post('http://ec2-52-24-108-177.us-west-2.compute.amazonaws.com:3030/flood/'', data={'query': statement})
    
    json = response.json()
    results = ""
    keys = json.get('head').get('vars')
    
    for r in json.get('results').get('bindings'):
        results = results + (",".join([str(r.get(key).get('value')) for key in keys]) + "\n")

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
