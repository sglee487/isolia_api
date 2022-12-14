from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request

from managers.auth import oauth2_app, oauth2_scheme
from managers.board import BoardManager
from models.enums import BoardType

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter(tags=['Board'])

@router.get('/board/{board_type}', dependencies=[Depends(oauth2_app)], status_code=HTTP_200_OK)
async def get_board_list(board_type: BoardType):
    return await BoardManager.get_board_list(board_type)

@router.post('/board/{board_type}', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_201_CREATED)
async def write_board(request: Request, board_type: BoardType):
    return await BoardManager.write_board(request, board_type)