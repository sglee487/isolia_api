from fastapi import APIRouter
from fastapi.params import Depends
from fastapi import File, UploadFile
from starlette.requests import Request
from databases.interfaces import Record

from managers.auth import oauth2_app, oauth2_scheme
from managers.board import BoardManager
from schemas.request.comment import CommentCreateIn
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from database.models.enums import BoardType

router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)


@router.post(
    "/{board_id}/",
    dependencies=[Depends(oauth2_scheme)],
    status_code=HTTP_201_CREATED,
)
async def post_comment(request: Request, board_id: int, comment_model: CommentCreateIn) -> int:
    user: Record = request.state.user
    return await BoardManager.post_comment(board_id, comment_model, user.id)
