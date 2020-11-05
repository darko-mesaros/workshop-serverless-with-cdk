import os
import json

def handler(event, context):
    region = os.environ.get('AWS_REGION')

    message = 'This is a hello from {}!'.format(region)  

    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }
