from fastapi import APIRouter

from resources import user, auth

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)