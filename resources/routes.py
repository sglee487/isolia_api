from fastapi import APIRouter

from resources import user, auth, board, comment

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(board.router)
api_router.include_router(comment.router)
