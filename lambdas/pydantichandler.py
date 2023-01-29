import json
import boto3
import os
from model import Model


def pydantic_lambda(event, context):
    print("event is: ")
    print(event)
    message_object = json.loads(event["body"])
    model = Model(**message_object)
    username = event["requestContext"]["authorizer"]["lambda"]["username"]
    model_object = {
        "id": str(model.id),
        "created_at": str(model.created_at),
        "item": model.item,
        "content": model.content,
        "username": username
    }
    client = boto3.client('sns')
    try:
        response = client.publish(
            TopicArn='arn:aws:sns:us-east-1:103162528131:yagel-sns',
            Message=json.dumps({'default': json.dumps(model_object)}),
            Subject='MessageToSns',
            MessageStructure='json'
        )
    except:
        error_object = {
            "message": "An error occurred publising to sns"
        }
        return {"statusCode": 500, "body": error_object}
    return {"statusCode": 200, "body": str(model_object)}
