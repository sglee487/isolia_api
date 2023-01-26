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
    "/",
    dependencies=[Depends(oauth2_scheme)],
    status_code=HTTP_201_CREATED,
)
async def post_comment(request: Request, comment_model: CommentCreateIn):
    user: Record = request.state.user
    return await BoardManager.post_comment(comment_model, user.id)
