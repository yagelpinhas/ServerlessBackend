import json
import boto3
import os
from model import Model

s3 = boto3.client('s3')


def delete_item_lambda(event, context):
    item = event["pathParameters"]["itemname"]
    username = event["requestContext"]["authorizer"]["lambda"]["username"]
    response = s3.delete_object(
        Bucket = os.environ["BUCKET_NAME"],
        Key = username+"/"+item
    )
    model_object = {'message': "Deleted The Item : {} From S3 BUCKET .".format(item), 'bucket_name': os.environ["BUCKET_NAME"],
                    'item': item,
                    'response': response
                    }
    return {"statusCode": 200, "body": str(model_object)}
