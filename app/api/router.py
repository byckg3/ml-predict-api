from fastapi import APIRouter
from app.api import heart

api_router = APIRouter( prefix="/api/disease" )
api_router.include_router( heart.router, tags = [ "Heart" ] )
