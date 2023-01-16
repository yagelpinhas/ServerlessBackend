import json
import os
import boto3
from utils.fucnction_utils import encrypt_password
client = boto3.client('dynamodb')


def register_lambda(event, context):
    username = json.loads(event["body"])["username"]
    password = json.loads(event["body"])["password"]
    encrypted_password = encrypt_password(password)
    successful_message = {
        "message": "Successfully Registered UserName: {}".format(username)
    }
    client.put_item(
        TableName=os.environ["TABLE_NAME"],
        Item ={
            "username": {"S": username},
            "password": {"S": encrypted_password}
        }
    )
    return {"statusCode": 200, "body": json.dumps(successful_message)}

