import json
import boto3
import os
from model import Model

s3 = boto3.client('s3')


def get_items_lambda(event, context):
    username = event["requestContext"]["authorizer"]["lambda"]["username"]
    response = s3.list_objects(Bucket=os.environ["BUCKET_NAME"], Prefix=username+"/")
    contents = response["Contents"]
    print("contents is: ")
    print(contents)
    print("type of contents is : ")
    print(type(contents))
    items = list(map(lambda item: item["Key"], contents))
    model_object = {"Objects": str(items)}
    return {"statusCode": 200, "body": json.dumps(model_object)}
