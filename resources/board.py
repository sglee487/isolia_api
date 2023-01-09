from fastapi import APIRouter
from fastapi.params import Depends

from managers.auth import oauth2_app
# from managers.board import BoardManager
from database.models.enums import BoardType

from starlette.status import HTTP_200_OK

router = APIRouter(tags=["Board"])


# @router.get(
#     "/board/{board_type}", dependencies=[Depends(oauth2_app)], status_code=HTTP_200_OK
# )
# async def get_board_list(board_type: BoardType):
#     return await BoardManager.get_board_list(board_type)
#
#
# @router.post(
#     "/board/{board_type}",
#     dependencies=[Depends(oauth2_scheme)],
#     status_code=HTTP_201_CREATED,
# )
# async def write_board(
#     request: Request, board_type: BoardType, post_data: BoardCreateIn
# ):
#     if (
#         request.state.user.role != RoleType.admin.value
#         and board_type != BoardType.suggestion
#     ):
#         return {"message": "You can't write this board."}
#     return await BoardManager.write_board(request, board_type, post_data.dict())
#
#
# @router.get(
#     "/board/{board_type}/{board_id}",
#     dependencies=[Depends(oauth2_app)],
#     status_code=HTTP_200_OK,
# )
# async def get_board(board_id: int):
#     return await BoardManager.get_board(board_id)


# made by copilot
# @router.delete('/board/{board_type}/{post_id}', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def delete_board(request: Request, board_type: BoardType, post_id: int):
#     if request.state.user.role != RoleType.admin.value and board_type != BoardType.suggestion:
#         return {"message": "You can't delete this board."}
#     return await BoardManager.delete_board(request, board_type, post_id)
#
# @router.put('/board/{board_type}/{post_id}/approve', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def approve_board(request: Request, board_type: BoardType, post_id: int):
#     if request.state.user.role != RoleType.admin.value and board_type != BoardType.suggestion:
#         return {"message": "You can't approve this board."}
#     return await BoardManager.approve_board(request, board_type, post_id)
#
# @router.put('/board/{board_type}/{post_id}/reject', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def reject_board(request: Request, board_type: BoardType, post_id: int):
#     if request.state.user.role != RoleType.admin.value and board_type != BoardType.suggestion:
#         return {"message": "You can't reject this board."}
#     return await BoardManager.reject_board(request, board_type, post_id)
#
# @router.put('/board/{board_type}/{post_id}/like', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def like_board(request: Request, board_type: BoardType, post_id: int):
#     return await BoardManager.like_board(request, board_type, post_id)
#
# @router.put('/board/{board_type}/{post_id}/unlike', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def unlike_board(request: Request, board_type: BoardType, post_id: int):
#     return await BoardManager.unlike_board(request, board_type, post_id)
#
# @router.put('/board/{board_type}/{post_id}/comment', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def comment_board(request: Request, board_type: BoardType, post_id: int, comment: str):
#     return await BoardManager.comment_board(request, board_type, post_id, comment)
#
# @router.put('/board/{board_type}/{post_id}/uncomment', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def uncomment_board(request: Request, board_type: BoardType, post_id: int, comment_id: int):
#     return await BoardManager.uncomment_board(request, board_type, post_id, comment_id)
#
# @router.put('/board/{board_type}/{post_id}/comment/like', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def like_comment_board(request: Request, board_type: BoardType, post_id: int, comment_id: int):
#     return await BoardManager.like_comment_board(request, board_type, post_id, comment_id)
#
# @router.put('/board/{board_type}/{post_id}/comment/unlike', dependencies=[Depends(oauth2_scheme)], status_code=HTTP_200_OK)
# async def unlike_comment_board(request: Request, board_type: BoardType, post_id: int, comment_id: int):
#     return await BoardManager.unlike_comment_board(request, board_type, post_id, comment_id)
