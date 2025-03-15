from datetime import datetime
import pytest
import pytest_asyncio
from app.models.heart import HeartDiseaseRecord
from app.models.db import MongoDB
from app.models.repository import DocumentRepository
from app.models.service import RecordService
from app.models.user import UserProfile

@pytest_asyncio.fixture( loop_scope = "module" )
async def setup_mongo():
    MongoDB.DB_NAME = "test"
    monogo = MongoDB()
    await monogo.init_beanie()

    yield

    await monogo.close()

@pytest_asyncio.fixture( loop_scope = "module" )
async def user_profile():
    profile = { 
        "name": "Mike",
        "email": f"mike{ datetime.now() }@email.com"
    }
    user_profile = UserProfile( **profile )

    return user_profile

@pytest.mark.db
@pytest.mark.asyncio( loop_scope = "module" )
async def test_timestamp_created_and_updated( setup_mongo, user_profile ):

    # save
    saved_profile = await user_profile.save()
    print( saved_profile )
    assert saved_profile.created_at is not None
    assert saved_profile.updated_at is not None
    
    # get
    profile = await UserProfile.get( saved_profile.id )
    # print( profile )
    assert profile.id is not None
    assert profile.created_at is not None
    assert profile.updated_at is not None

    # update
    repository = DocumentRepository( UserProfile )
    updated_profile = await repository.update_by_id( saved_profile.id, { "name": "John" } )
    # print( updated_profile )
    assert updated_profile.created_at == profile.created_at
    assert updated_profile.updated_at > profile.updated_at

    deleted_count = await repository.delete_all()
    assert deleted_count >= 0, f"failed: Expected >= 0 but got { deleted_count }"