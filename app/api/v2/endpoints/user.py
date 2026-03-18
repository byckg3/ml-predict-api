from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.dependencies.service import user_service
from app.user.schemas import UserProfile, example
from app.user.services import UserService

router = APIRouter( prefix = "/user", )

ServiceDependency = Annotated[ UserService, Depends( user_service ) ]

@router.get( "/profile/{id}" )
async def get_profile( id: str, service: ServiceDependency ):

    pass

@router.get( "/profiles" )
async def get_all_profiles( service: ServiceDependency, page: int = 1, page_size: int = 10 ):
    
    pass

@router.post( "/login" )
async def login( service: ServiceDependency, 
                 login_info: dict[ str, Any ] = Body( example = example[ "login_info" ] ) ):
    
    pass

@router.post( "/profile", status_code = status.HTTP_201_CREATED )
async def save_profile( service: ServiceDependency, 
                        profile: UserProfile = Body( example = example[ "created_profile" ] ) ):
    
    pass

@router.put( "/profile/{id}" )
async def put_profile( id: str, service: ServiceDependency, 
                      patch: dict[ str, Any ] = Body( example = { "name": "John" } ) ):

    pass
        
@router.patch( "/profile/{id}" )
async def update_profile( id: str, service: ServiceDependency, 
                         patch: dict[ str, Any ] = Body( example = { "email": "test123@email.com" } ) ):

    pass

@router.delete( "/profile/{id}", status_code = status.HTTP_204_NO_CONTENT )
async def delete_profile( id: str, service: ServiceDependency ):

    pass

@router.delete( "/profiles", status_code = status.HTTP_204_NO_CONTENT )
async def delete_all_profiles( service: ServiceDependency ):

    pass