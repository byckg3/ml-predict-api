import traceback
from typing import Annotated, Any
from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.api.v1.controller import DocumentController
from app.api.dependencies.service import user_profile_service
from app.services.nosql import DocumentService
from app.services.user import UserProfileService
from app.user.v1.schemas import UserProfile, example

router = APIRouter( prefix = "/user", )

ServiceDependency = Annotated[ UserProfileService, Depends( user_profile_service ) ]

@router.get( "/profile/{id}" )
async def get_profile( id: str, service: ServiceDependency ):

    return await DocumentController.get_document( id, service )


@router.get( "/profiles" )
async def get_all_profiles( service: ServiceDependency, page: int = 1, page_size: int = 10 ):
    
    return await DocumentController.get_all_documents( service, page, page_size )


@router.post( "/login" )
async def login( service: ServiceDependency, 
                 login_info: dict[ str, Any ] = Body( examples = [ example[ "login_info" ] ] ) ):
    
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
                        profile: UserProfile = Body( examples = [ example[ "created_profile" ] ] ) ):
    
    return await DocumentController.save_document( profile, service )


@router.put( "/profile/{id}" )
async def put_profile( id: str, service: ServiceDependency, 
                      patch: dict[ str, Any ] = Body( examples = [ { "name": "John" } ] ) ):

    return await DocumentController.update_document( id, patch, service )
    
    
@router.patch( "/profile/{id}" )
async def update_profile( id: str, service: ServiceDependency, 
                         patch: dict[ str, Any ] = Body( examples = [ { "email": "test123@email.com" } ] ) ):

    return await put_profile( id, service, patch )


@router.delete( "/profile/{id}", status_code = status.HTTP_204_NO_CONTENT )
async def delete_profile( id: str, service: ServiceDependency ):

    return await DocumentController.delete_document( id, service )


@router.delete( "/profiles", status_code = status.HTTP_204_NO_CONTENT )
async def delete_all_profiles( service: ServiceDependency ):

    return await DocumentController.delete_all_document( service )