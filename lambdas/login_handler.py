import json
import boto3
import os
import jwt
from utils.fucnction_utils import encrypt_password
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')


def login_lambda(event, context):
    secret_name = "magic_word"
    region_name = "us-east-1"
    sts = boto3.client("sts")
    response = sts.assume_role(
        RoleArn="arn:aws:iam::103162528131:role/access-to-secrets-manager",
        RoleSessionName="learnaws-test-session"
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
    username = json.loads(event["body"])["username"]
    password = json.loads(event["body"])["password"]
    response = client.get_item(TableName=os.environ["TABLE_NAME"], Key={
        "username": {
            'S': username
        }
    })
    if "Item" in response.keys():
        if encrypt_password(password) == response["Item"]["password"]["S"]:
            encoded_jwt = jwt.encode({"username": username}, secret, algorithm="HS256")
            jwt_object = {
                "jwt": encoded_jwt
            }
            return {"statusCode": 200, "body": json.dumps(jwt_object)}
    error_msg = {
        "message": "Invalid username or password"
    }
    return {"statusCode": 401, "body": json.dumps(error_msg)}
