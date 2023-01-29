import json
import boto3
import os
s3 = boto3.client('s3')


def store_content(event, context):
    body = dict(bucket=os.environ["BUCKET_NAME"], input=event)
    event_received = json.loads(event["Records"][0]["body"])
    input_object = json.loads(event_received["Message"])
    s3.put_object(Bucket=os.environ["BUCKET_NAME"], Key=input_object["username"]+"/"+input_object["item"], Body=input_object["content"])
    return {"statusCode": 200, "body": json.dumps(body)}


