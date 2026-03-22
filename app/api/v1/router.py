from fastapi import APIRouter
from app.api.v1.endpoints import chat, heart, liver, user

v1_router = APIRouter( prefix = "/v1" )

v1_router.include_router( heart.router, tags = [ "v1 - Heart" ] )
v1_router.include_router( liver.router, tags = [ "v1 - Liver" ] )
v1_router.include_router( user.router, tags = [ "v1 - User" ] )
v1_router.include_router( chat.router, tags = [ "v1 - Chat" ] )