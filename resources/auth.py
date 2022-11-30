from fastapi import APIRouter
from fastapi.params import Depends

from managers.auth import oauth2_app
from managers.user import UserManager
from schemas.request.user import UserRegisterIn, UserSignIn

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from schemas.response.user import UserSignOut

router = APIRouter(tags=['Auth'])


@router.post('/user/', dependencies=[Depends(oauth2_app)], response_model=UserSignOut, status_code=HTTP_201_CREATED)
async def register(user_data: UserRegisterIn):
    return await UserManager.register(user_data.dict())


@router.post("/login/", dependencies=[Depends(oauth2_app)], status_code=HTTP_200_OK)
async def login(user_data: UserSignIn):
    return await UserManager.login(user_data.dict())
