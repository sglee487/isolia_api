from datetime import datetime

from asyncpg import UniqueViolationError
from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from decouple import config
from starlette.status import HTTP_400_BAD_REQUEST

from database.db import database
from database.models import user
from database.models.enums import LoginType
from schemas.base import EmailField


class UserDBManager:
    @staticmethod
    async def create_user(user_data: dict):
        try:
            id_ = database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(
                HTTP_400_BAD_REQUEST, "User with this login type & email already exists"
            )
        return await database.fetch_one(user.select().where(user.c.id == id_))

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    async def update_user(user: dict):
        try:
            if user['login_type'] == LoginType.email:
                update_expression = "SET display_name = :display_name, password = :new_password, updated_at = :updated_at"
                expression_attribute_values = {
                    ':display_name': user['display_name'],
                    ':new_password': user['password'],
                    ':updated_at': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                }
            elif user['login_type'] == LoginType.google:
                update_expression = "SET display_name = :display_name, updated_at = :updated_at"
                expression_attribute_values = {
                    ':display_name': user['display_name'],
                    ':updated_at': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                }
            else:
                raise Exception("Invalid login type")
            response = table.update_item(
                Key={'email': user['email'], 'login_type': user['login_type'].value},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            return response['Attributes']
        except ClientError as e:
            return JSONResponse(content=e.response["Error"], status_code=500)
