from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

from database.db import dynamodb
from decouple import config

table = dynamodb.Table(config("DB_USER_TABLE_NAME"))


async def create_user(user: dict):
    try:
        table.put_item(Item=user)
        return user
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


async def get_user(id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("id").eq(id)
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


async def get_users():
    try:
        response = table.scan(
            Limit=5,
            AttributesToGet=["username", "id"]
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


async def delete_user(user: dict):
    try:
        response = table.delete_item(
            Key={
                "id": user["id"],
                "created_at": user["created_at"]
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


async def update_user(user: dict):
    try:
        response = table.update_item(
            Key={
                "id": user["id"],
                "created_at": user["created_at"]
            },
            UpdateExpression="SET username = :username, age = :age",
            ExpressionAttributeValues={
                ":username": user["username"],
                ":age": user["age"]
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
