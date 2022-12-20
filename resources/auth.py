from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request

from managers.auth import oauth2_app, oauth2_scheme
from managers.user import UserManager
from schemas.request.user import UserRegisterIn, UserSignIn, UserUpdateIn

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from schemas.response.user import UserResponse, UserDisplayNameResponse

router = APIRouter(tags=["Auth"])


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
    response_model=UserDisplayNameResponse,
    status_code=HTTP_200_OK,
)
async def update_user(request: Request, user_data: UserUpdateIn):
    user = request.state.user
    return await UserManager.update(user_data.dict(), user)


@router.post(
    "/login/",
    dependencies=[Depends(oauth2_app)],
    response_model=UserResponse,
    status_code=HTTP_200_OK,
)
async def login(user_data: UserSignIn):
    return await UserManager.login(user_data.dict())


@router.get(
    "/token/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=UserResponse,
    status_code=HTTP_200_OK,
)
async def login_with_token(request: Request):
    user = request.state.user
    return await UserManager.check_token(
        {
            "token": request.state.token,
            "id": user.id,
            "login_type": user["login_type"],
            "email": user["email"],
            "display_name": user["display_name"],
            "role": user["role"],
        }
    )
