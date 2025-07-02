from fastapi import APIRouter
from src.api.endpoints import users, auth, ads, comments

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(ads.router, prefix="/ads", tags=["ads"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
