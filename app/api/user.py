from typing import Annotated, Any
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Request, status
from app.api.controller import DocumentController
from app.models.service import DocumentService, RecordService
from app.models.user import UserProfile, _example_value

def user_profile_service( request: Request ) -> DocumentService:

    user_profile_service = None
    if hasattr( request.app.state, "user_profile_service" ):
        user_profile_service = request.app.state.user_profile_service
    else:
        user_profile_service = DocumentService( UserProfile )
        request.app.state.user_profile_service = user_profile_service

    return user_profile_service

ServiceDependency = Annotated[ RecordService, Depends( user_profile_service ) ]

router = APIRouter( prefix = "/user" )

@router.get( "/profile/{id}" )
async def get_profile( id: PydanticObjectId, service: ServiceDependency ) -> UserProfile:

    return await DocumentController.get_document( id, service )

@router.get( "/profiles" )
async def get_all_profiles( service: ServiceDependency, page: int = 1, page_size: int = 10 ) -> list[ UserProfile ]:
    
    return await DocumentController.get_all_documents( service, page, page_size )

@router.post( "/profile", status_code = status.HTTP_201_CREATED )
async def save_profile( service: ServiceDependency, 
                        profile: UserProfile = Body( ..., example = _example_value ) ) -> UserProfile:
    
    return await DocumentController.save_document( profile, service )

@router.put( "/profile/{id}" )
async def put_profile( id: PydanticObjectId, service: ServiceDependency, 
                      patch: dict[ str, Any ] = Body( ..., example = { "name": "John" } ) ) -> UserProfile:

    return await DocumentController.update_document( id, patch, service )
        
@router.patch( "/profile/{id}" )
async def update_profile( id: PydanticObjectId, service: ServiceDependency, 
                         patch: dict[ str, Any ] = Body( ..., example = { "email": "test123@email.com" } ) ) -> UserProfile:

    return await put_profile( id, service, patch )

@router.delete( "/profile/{id}", status_code = status.HTTP_204_NO_CONTENT )
async def delete_profile( id: PydanticObjectId, service: ServiceDependency ) -> None:

    return await DocumentController.delete_document( id, service )

@router.delete( "/profiles", status_code = status.HTTP_204_NO_CONTENT )
async def delete_all_profiles( service: ServiceDependency ) -> None:

    return await DocumentController.delete_all_document( service )