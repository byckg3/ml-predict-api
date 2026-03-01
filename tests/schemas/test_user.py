import pytest
from typing import Any

from app.repositories.nosql import DocumentRepository
from app.schemas.user import UserProfile, example


@pytest.fixture( scope = "module" )
async def user_profile( setup_mongo ):
    data: dict[ Any, Any ] = example[ "created_profile" ]
    user_profile = UserProfile( **data )

    return user_profile


@pytest.mark.db
async def test_timestamp_created_and_updated( user_profile ):

    # save
    saved_profile = await user_profile.save()
    # print( saved_profile )
    assert saved_profile.created_at is not None
    assert saved_profile.updated_at is not None
    
    # get
    profile = await UserProfile.get( saved_profile.id )
    # print( profile )
    assert profile is not None
    assert profile.id is not None
    assert profile.created_at is not None
    assert profile.updated_at is not None

    # update
    repository = DocumentRepository( UserProfile )
    updated_profile = await repository.update_by_id( saved_profile.id, { "name": "John" } )
    # print( updated_profile )
    
    assert updated_profile is not None
    assert updated_profile.created_at == profile.created_at
    assert updated_profile.updated_at > profile.updated_at

    # find one
    finded_profile = await repository.find_one( UserProfile.email == user_profile.email )
    # print( finded_profile )
    
    assert finded_profile is not None
    assert finded_profile.email == user_profile.email


    deleted_count = await repository.delete_all()
    assert deleted_count >= 0, f"failed: Expected >= 0 but got { deleted_count }"