from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request

from managers.auth import oauth2_app, oauth2_scheme
from managers.user import UserManager
from schemas.request.user import UserRegisterIn, UserSignIn, UserUpdateIn

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from schemas.response.user import UserResponse, UserDisplayNameResponse

router = APIRouter(tags=["Auth"])


@router.get(
    "/token/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=UserResponse,
    status_code=HTTP_200_OK,
)
async def login_with_token(request: Request):
    user = request.state.user
    token = request.state.token
    exp = request.state.exp
    return await UserManager.get_user_response(
        {
            "token": token,
            "exp": exp,
            "id": user["id"],
            "login_type": user["login_type"],
            "email": user["email"],
            "picture_32": user["picture_32"],
            "picture_96": user["picture_96"],
            "display_name": user["display_name"],
            "role": user["role"],
        }
    )
