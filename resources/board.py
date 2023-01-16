from fastapi import APIRouter
from fastapi.params import Depends
from fastapi import File, UploadFile
from starlette.requests import Request

from managers.auth import oauth2_app, oauth2_scheme
from managers.board import BoardManager
from schemas.request.user import UserRegisterIn, UserSignIn, UserUpdateIn
from schemas.response.user import ProfilePictureResponse

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from schemas.response.user import UserResponse, UserDisplayNameResponse

router = APIRouter(
    prefix="/board",
    tags=["Board"]
)


@router.post(
    "/images/",
    dependencies=[Depends(oauth2_scheme)],
    # response_model=ProfilePictureResponse,
    # status_code=HTTP_201_CREATED,
)
async def upload_image_files(files: list[UploadFile] = File(...)):
    return await BoardManager.upload_images(files)
