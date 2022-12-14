from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request

from managers.auth import oauth2_app, oauth2_scheme
from managers.user import UserManager
from models.enums import BoardType

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter(tags=['Board'])

@router.get('/board/{board_type}', dependencies=[Depends(oauth2_app)], status_code=HTTP_200_OK)
async def get_board_list(request: Request, board_type: BoardType):
    print(request)
    print(board_type)
    # user = request.state.user
    # return await UserManager.get_board_list(board_type, user)
