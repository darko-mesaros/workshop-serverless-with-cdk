import os
import json
import boto3

def handler(event, context):
    table = os.environ.get('table')
    dynamodb = boto3.client('dynamodb')

    item = {
            "name":{'S':event["queryStringParameters"]["name"]},
            "location":{'S':event["queryStringParameters"]["location"]},
            "age":{'S':event["queryStringParameters"]["age"]}
            }

    
    response = dynamodb.put_item(TableName=table,
            Item=item
            )

    message = 'Status of the write to DynamoDB {}!'.format(response)  
    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }
