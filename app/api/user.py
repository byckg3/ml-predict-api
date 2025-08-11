import traceback
from typing import Annotated, Any
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.api.controller import DocumentController
from app.api.dependencies import user_profile_service, verify_jwt
from app.services.nosql import DocumentService
from app.services.user import UserProfileService
from app.schemas.user import UserProfile, example

router = APIRouter( prefix = "/user", )

ServiceDependency = Annotated[ UserProfileService, Depends( user_profile_service ) ]

@router.get( "/profile/{id}" )
async def get_profile( id: PydanticObjectId, service: ServiceDependency ) -> UserProfile:

    return await DocumentController.get_document( id, service )

@router.get( "/profiles" )
async def get_all_profiles( service: ServiceDependency, page: int = 1, page_size: int = 10 ) -> list[ UserProfile ]:
    
    return await DocumentController.get_all_documents( service, page, page_size )

@router.post( "/login" )
async def login( service: ServiceDependency, 
                 login_info: dict[ str, Any ] = Body( example = example[ "login_info" ] ) ) -> UserProfile:
    
    try:
        user_profile = await service.find_by_email( login_info[ "email" ] )
        if user_profile:
            return JSONResponse( content = jsonable_encoder( user_profile ), 
                                 status_code = status.HTTP_200_OK )     
    except Exception as e:
        print( e )
        print( traceback.format_exc() )
    
    return JSONResponse( content = { "message": "Invalid credentials" }, 
                         status_code = status.HTTP_401_UNAUTHORIZED )

@router.post( "/profile", status_code = status.HTTP_201_CREATED )
async def save_profile( service: ServiceDependency, 
                        profile: UserProfile = Body( example = example[ "created_profile" ] ) ) -> UserProfile:
    
    return await DocumentController.save_document( profile, service )

@router.put( "/profile/{id}" )
async def put_profile( id: PydanticObjectId, service: ServiceDependency, 
                      patch: dict[ str, Any ] = Body( example = { "name": "John" } ) ) -> UserProfile:

    return await DocumentController.update_document( id, patch, service )
        
@router.patch( "/profile/{id}" )
async def update_profile( id: PydanticObjectId, service: ServiceDependency, 
                         patch: dict[ str, Any ] = Body( example = { "email": "test123@email.com" } ) ) -> UserProfile:

    return await put_profile( id, service, patch )

@router.delete( "/profile/{id}", status_code = status.HTTP_204_NO_CONTENT )
async def delete_profile( id: PydanticObjectId, service: ServiceDependency ) -> None:

    return await DocumentController.delete_document( id, service )

@router.delete( "/profiles", status_code = status.HTTP_204_NO_CONTENT )
async def delete_all_profiles( service: ServiceDependency ) -> None:

    return await DocumentController.delete_all_document( service )