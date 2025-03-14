from fastapi import APIRouter
from app.api import heart, liver, user

api_router = APIRouter( prefix="/api" )
api_router.include_router( heart.router, tags = [ "Heart" ] )
api_router.include_router( liver.router, tags = [ "Liver" ] )
api_router.include_router( user.router, tags = [ "User" ] )