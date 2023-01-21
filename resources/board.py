from fastapi import APIRouter
from fastapi.params import Depends
from fastapi import File, UploadFile
from starlette.requests import Request
from databases.interfaces import Record

from managers.auth import oauth2_app, oauth2_scheme
from managers.board import BoardManager
from schemas.request.board import BoardCreateIn
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from database.models.enums import BoardType

router = APIRouter(
    prefix="/board",
    tags=["Board"]
)


@router.post(
    "/images/",
    dependencies=[Depends(oauth2_scheme)],
    status_code=HTTP_201_CREATED,
)
async def upload_image_files(request: Request, files: list[UploadFile] = File(...)) -> list[str]:
    user = request.state.user
    return await BoardManager.upload_images(files, user.id)


@router.post(
    "/",
    dependencies=[Depends(oauth2_scheme)],
)
async def post_board(request: Request, board_model: BoardCreateIn):
    user: Record = request.state.user
    return await BoardManager.post_board(board_model, user.id)


@router.get(
    "/post/{post_id}",
    dependencies=[Depends(oauth2_app)],
    status_code=HTTP_200_OK,
)
async def get_post(post_id: int):
    return await BoardManager.get_post(post_id)


@router.get(
    "/all/",
    dependencies=[Depends(oauth2_app)],
    status_code=HTTP_200_OK,
)
async def get_board_list(page: int = 1):
    return await BoardManager.get_board_list(None, page)


@router.get(
    "/{board_type}/",
    dependencies=[Depends(oauth2_app)],
    status_code=HTTP_200_OK,
)
async def get_board_list(board_type: BoardType, page: int = 1):
    return await BoardManager.get_board_list(board_type, page)
