import json
import boto3
import os
import jwt
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')


def authorizer_lambda(event, context):
    print("the event in authorizer is : ")
    print(event)
    print("event headers is : ")
    print(event["headers"])
    encoded_jwt = event["headers"]["authorization"]
    print("encoded jwt is : ")
    print(encoded_jwt)
    secret_name = "magic_word"
    region_name = "us-east-1"
    sts = boto3.client("sts")
    response = sts.assume_role(
        RoleArn="arn:aws:iam::103162528131:role/access-to-secrets-manager",
        RoleSessionName="auth"
    )
    new_session = boto3.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                aws_session_token=response['Credentials']['SessionToken'])
    session_client = new_session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = session_client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    secret = json.loads(get_secret_value_response["SecretString"])["magic_word"]
    decoded_jwt = jwt.decode(encoded_jwt.split()[1], secret, algorithms=["HS256"])
    if "username" in decoded_jwt.keys():
        username = decoded_jwt["username"]
        response = dynamodb.get_item(TableName=os.environ["TABLE_NAME"], Key={
            "username": {
                'S': username
            }
        })
        if "Item" in response.keys():
            return {
                "principalId": 'anonymous',
                "policyDocument": {
                    "Version": '2012-10-17',
                    "Statement": [
                        {
                            "Action": 'execute-api:Invoke',
                            "Effect": 'Allow',
                            "Resource": event["routeArn"],
                        },
                    ],
                },
                "context":{
                    "username": username
                }
            }
    return {"statusCode": 403, "body": json.dumps({"message": "bad token"})}
