from datetime import datetime

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from decouple import config
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from database.db import database
from database.models import user
from database.models.enums import LoginType
from schemas.base import EmailField


class UserDBManager:
    @staticmethod
    async def create_user(user_data: dict):
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(
                HTTP_400_BAD_REQUEST, "User with this login type & email already exists"
            )
        return await database.fetch_one(user.select().where(user.c.id == id_))

    @staticmethod
    async def get_user(login_type: LoginType, email: EmailField):
        try:
            user_do = await database.fetch_one(
                user.select()
                .where(user.c.email == email)
                .where(user.c.login_type == login_type)
            )
            return user_do
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def deactivate_user(user_data: dict):
        try:
            id_ = await database.execute(
                user.update()
                .where(user.c.id == user_data["id"])
                .values(activate=False)
                .values(deleted_at=datetime.now())
            )
            return id_
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def activate_user(user_data: dict):
        try:
            id_ = await database.execute(
                user.update()
                .where(user.c.id == user_data["id"])
                .values(activate=True)
                .values(deleted_at=None)
            )
            return id_
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def delete_user(user_data: dict):
        try:
            id_ = await user.delete().where(user.c.id == user_data["id"])
            return id_
        except Exception as e:
            return JSONResponse(content=e, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def update_user(user_data: dict, user_id: int):
        id_ = await database.execute(
            user.update().where(user.c.id == user_id).values(**user_data)
        )
        return id_
        # try:
        #     if user['login_type'] == LoginType.email:
        #         update_expression = "SET display_name = :display_name, password = :new_password, updated_at = :updated_at"
        #         expression_attribute_values = {
        #             ':display_name': user['display_name'],
        #             ':new_password': user['password'],
        #             ':updated_at': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #         }
        #     elif user['login_type'] == LoginType.google:
        #         update_expression = "SET display_name = :display_name, updated_at = :updated_at"
        #         expression_attribute_values = {
        #             ':display_name': user['display_name'],
        #             ':updated_at': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #         }
        #     else:
        #         raise Exception("Invalid login type")
        #     response = table.update_item(
        #         Key={'email': user['email'], 'login_type': user['login_type'].value},
        #         UpdateExpression=update_expression,
        #         ExpressionAttributeValues=expression_attribute_values,
        #         ReturnValues="ALL_NEW"
        #     )
        #     return response['Attributes']
        # except ClientError as e:
        #     return JSONResponse(content=e.response["Error"], status_code=500)
