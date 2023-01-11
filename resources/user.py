from fastapi import APIRouter
from fastapi.params import Depends
from fastapi import File, UploadFile
from starlette.requests import Request

from managers.auth import oauth2_app, oauth2_scheme
from managers.user import UserManager
from schemas.base import ProfilePicture
from schemas.request.user import UserRegisterIn, UserSignIn, UserUpdateIn

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from schemas.response.user import UserResponse, UserDisplayNameResponse
router = APIRouter(tags=["Users"])


@router.post(
    "/user/",
    dependencies=[Depends(oauth2_app)],
    response_model=UserResponse,
    status_code=HTTP_201_CREATED,
)
async def register(user_data: UserRegisterIn):
    return await UserManager.register(user_data.dict())


@router.patch(
    "/user/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=UserResponse,
    status_code=HTTP_200_OK,
)
async def update_user(request: Request, user_update_data: UserUpdateIn):
    user = request.state.user
    token = request.state.token
    exp = request.state.exp
    return await UserManager.update(user_update_data.dict(), user, token, exp)


@router.post(
    "/login/",
    dependencies=[Depends(oauth2_app)],
    response_model=UserResponse,
    status_code=HTTP_200_OK,
)
async def login(user_data: UserSignIn):
    return await UserManager.login(user_data.dict())

@router.post(
    "/upload/profile_picture/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=ProfilePicture,
    status_code=HTTP_201_CREATED,
)
async def upload_profile_picture(file: UploadFile = File(...)):
    return await UserManager.upload_profile_picture(file)