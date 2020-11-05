import os
import json
import boto3

def handler(event, context):
    table = os.environ.get('table')
    dynamodb = boto3.client('dynamodb')

    key = {
            "name":{'S':event["queryStringParameters"]["name"]}
            }

    response = dynamodb.get_item(TableName=table,
            Key=key
            )

    return {
        "statusCode": 200,
        "body": json.dumps(response["Item"])
    }
