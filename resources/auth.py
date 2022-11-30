from fastapi import APIRouter
from fastapi.params import Depends

from managers.auth import oauth2_app
from managers.user import UserManager
from schemas.request.user import UserRegisterIn, UserSignIn

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter(tags=['Auth'])


@router.post('/user/', dependencies=[Depends(oauth2_app)], status_code=HTTP_201_CREATED)
async def register(user_data: UserRegisterIn):
    token = await UserManager.register(user_data.dict())
    return {"token": token}


@router.post("/login/", dependencies=[Depends(oauth2_app)], status_code=HTTP_200_OK)
async def login(user_data: UserSignIn):
    token = await UserManager.login(user_data.dict())
    return {"token": token}
