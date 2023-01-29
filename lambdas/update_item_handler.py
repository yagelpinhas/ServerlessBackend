import json
import boto3
import os
from model import Model

s3 = boto3.client('s3')


def update_item_lambda(event, context):
    username = event["requestContext"]["authorizer"]["lambda"]["username"]
    print("event is : ")
    print(event)
    item = event["pathParameters"]["itemname"]
    message_object = json.loads(event["body"])
    print("message object is : ")
    print(message_object)
    new_content = message_object["content"]
    print("item to update is : ")
    print(item)
    print("the new content is : ")
    print(new_content)
    s3.put_object(Bucket=os.environ["BUCKET_NAME"], Key=username+"/"+item, Body=new_content)
    model_object = {'message': "Updated The Item : {} With the new content {}.".format(item, new_content),
                    'bucket_name': os.environ["BUCKET_NAME"]}
    return {"statusCode": 200, "body": str(model_object)}
