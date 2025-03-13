from fastapi import APIRouter
from app.api import heart, liver

api_router = APIRouter( prefix="/api/disease" )
api_router.include_router( heart.router, tags = [ "Heart" ] )
api_router.include_router( liver.router, tags = [ "Liver" ] )