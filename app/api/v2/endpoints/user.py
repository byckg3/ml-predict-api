from typing import Annotated, Any
from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.api.dependencies.service import user_service
from app.user.models import User
from app.user.v2.schemas import UserProfile, UserPatch, examples
from app.user.services import UserService

router = APIRouter( prefix = "/user", )

ServiceDependency = Annotated[ UserService, Depends( user_service ) ]

@router.get( "/profile/{id}", response_model = UserProfile )
async def get_profile( id: str, service: ServiceDependency ):

    user = await service.find_by_id( id )
    if not user:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, 
                             detail = "User not found" )
    
    return user


@router.get( "/profiles", response_model = list[ UserProfile ] )
async def get_all_profiles( service: ServiceDependency, page: int = 1, page_size: int = 10 ):
    
    skip_count = ( page - 1 ) * page_size
    limit_count = page_size
    
    users = await service.find_all( offset = skip_count, limit = limit_count )
    
    return users


@router.post( "/login", response_model = UserProfile )
async def login( service: ServiceDependency, 
                 login_info: dict[ str, Any ] = Body( example = examples[ "login_info" ] ) ):
    
    user = await service.find_by_email( login_info.get( "email", "" ) )
    if not user:
        raise HTTPException( status_code = status.HTTP_401_UNAUTHORIZED, 
                             detail = "Invalid credentials" )
    
    return user
    

@router.post( "/profile", response_model = UserProfile, status_code = status.HTTP_201_CREATED )
async def save_profile( service: ServiceDependency, 
                        base_profile: UserPatch = Body( example = examples[ "base_profile" ] ) ):
    
    new_user = await service.save( User( **base_profile.model_dump() ) )
    
    return new_user


@router.put( "/profile/{id}", response_model = UserProfile )
async def put_profile( id: str, service: ServiceDependency, 
                       patch: UserPatch = Body( example = { "name": "John" } ) ):
    
    updated_content = patch.model_dump( exclude_unset = True )
    update_profile = await service.update_by_id( id, updated_content )
    
    if not update_profile:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, 
                             detail = "User not found" )
    
    return update_profile


@router.patch( "/profile/{id}", response_model = UserProfile )
async def update_profile( id: str, service: ServiceDependency, 
                          patch: UserPatch = Body( example = { "email": "test123@email.com" } ) ):

    return await put_profile( id, service, patch )


@router.delete( "/profile/{id}", status_code = status.HTTP_204_NO_CONTENT )
async def delete_profile( id: str, service: ServiceDependency ):

    deleted_count = await service.delete_by_id( id )
    
    if deleted_count == 0:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, 
                             detail = "User not found" )
    

@router.delete( "/profiles", status_code = status.HTTP_204_NO_CONTENT )
async def delete_all_profiles( service: ServiceDependency ):

    deleted_count = await service.delete_all()
    
    if deleted_count == 0:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, 
                             detail = "No users found" )
    