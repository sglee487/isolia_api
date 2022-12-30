from datetime import datetime

from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

from database.db import dynamodb
from decouple import config

from models.enums import LoginType, RoleType
from schemas.base import EmailField

table = dynamodb.Table(config("DB_USER_TABLE_NAME"))


async def create_user(user: dict):
    try:
        table.put_item(Item=user)
        return user
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


async def get_user(login_type: LoginType, email: EmailField):
    try:
        response = table.get_item(
            Key={'email': email, 'login_type': login_type.value}
        )
        return response["Item"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    except Exception as e:
        print(e)


async def deactivate_user(user: dict):
    try:
        response = table.update_item(
            Key={'email': user['email'], 'login_type': user['login_type'].value},
            UpdateExpression="SET is_active = :is_active",
            ExpressionAttributeValues={
                ':is_active': False,
                ':deleted_at': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


async def activate_user(user: dict):
    try:
        response = table.update_item(
            Key={'email': user['email'], 'login_type': user['login_type'].value},
            UpdateExpression="SET is_active = :is_active",
            ExpressionAttributeValues={
                ':is_active': True,
                ':deleted_at': None
            }
        )
        return response
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
            Key={'email': user['email'], 'login_type': user['login_type'].value},
            UpdateExpression="SET display_name = :display_name, password = :new_password, updated_at = :updated_at",
            ExpressionAttributeValues={
                ':display_name': user['display_name'],
                ':new_password': user['password'],
                ':updated_at': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            },
            ReturnValues="ALL_NEW"
        )
        return response['Attributes']
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
