from fastapi import APIRouter, Depends
from app.api import chat, heart, liver, user
from app.auth.dependencies.csrf_utils import verify_csrf_token
from app.auth.dependencies.jwt_utils import verify_jwt
from app.auth import google

api_router = APIRouter( prefix = "/api", dependencies = [ Depends( verify_csrf_token ), Depends( verify_jwt ),  ] )
api_router.include_router( heart.router, tags = [ "Heart" ] )
api_router.include_router( liver.router, tags = [ "Liver" ] )
api_router.include_router( user.router, tags = [ "User" ] )
api_router.include_router( chat.router, tags = [ "Chat" ] )