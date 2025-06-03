from fastapi import APIRouter, Depends
from app.api import chat, heart, liver, user
from app.api.dependencies import verify_jwt_token

api_router = APIRouter( prefix="/api", dependencies = [ Depends( verify_jwt_token ) ] )
api_router.include_router( heart.router, tags = [ "Heart" ] )
api_router.include_router( liver.router, tags = [ "Liver" ] )
api_router.include_router( user.router, tags = [ "User" ] )
api_router.include_router( chat.router, tags = [ "Chat" ] )