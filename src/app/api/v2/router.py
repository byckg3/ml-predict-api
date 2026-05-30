from fastapi import APIRouter, Depends
from app.api.v2.endpoints import user

v2_router = APIRouter( prefix = "/v2" )

v2_router.include_router( user.router, tags = [ "v2 - User" ] )