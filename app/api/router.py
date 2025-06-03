from fastapi import APIRouter, Depends
from app.api import heart, liver, user
from app.api.dependencies import verify_jwt_from_header

api_router = APIRouter( prefix="/api", dependencies = [ Depends( verify_jwt_from_header ) ] )
api_router.include_router( heart.router, tags = [ "Heart" ] )
api_router.include_router( liver.router, tags = [ "Liver" ] )
api_router.include_router( user.router, tags = [ "User" ] )