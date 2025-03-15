
import pytest
import pytest_asyncio
from app.models.heart import HeartDiseaseRecord, example_record
from app.models.db import MongoDB
from app.models.service import RecordService

@pytest_asyncio.fixture( loop_scope = "module" )
async def setup_mongo():
    MongoDB.DB_NAME = "test"
    monogo = MongoDB()
    await monogo.init_beanie()

    yield

    await monogo.close()

@pytest_asyncio.fixture( loop_scope = "module" )
async def heart_record_service():
    heart_record_service = RecordService( HeartDiseaseRecord )

    return heart_record_service

@pytest.mark.db
@pytest.mark.asyncio( loop_scope = "module" )
async def test_service_crud_operations( setup_mongo, heart_record_service ):

    heart_record = HeartDiseaseRecord( **example_record )

    # save
    save_result = await heart_record_service.save( heart_record )
    # print( save_result )
    assert save_result.id is not None
    assert save_result.id == heart_record.id
    
    # update
    update_result = await heart_record_service.update_by_id( heart_record.id, { "features.age": 67, "features.target": 1 } )
    # print( update_result )
    assert update_result.features.age == 67
    assert update_result.features.target == 1
    
    # find recordss
    records = await heart_record_service.find_by_user_id( heart_record.user_id, limit = 20 )
    # print( records )
    assert len( records ) > 0, f"failed: Expected > 0 but got { len( records ) }"

     # get
    get_result = await heart_record_service.get_by_id( heart_record.id )
    assert get_result.id is not None
    assert get_result.id == heart_record.id

    # delete
    deleted_count = await heart_record_service.delete_by_id( heart_record.id )
    assert deleted_count == 1, f"failed: Expected 1 but got { deleted_count }"

    # get empty
    get_empty_result = await heart_record_service.get_by_id( heart_record.id )
    assert get_empty_result is None

@pytest.mark.db
@pytest.mark.asyncio( loop_scope = "module" )
async def test_service_delete_all_documents( setup_mongo, heart_record_service ):

    deleted_count = await heart_record_service.delete_all()
    assert deleted_count >= 0, f"failed: Expected >= 0 but got { deleted_count }"

    empty_list = await heart_record_service.find_all()
    assert len( empty_list ) == 0, f"failed: Expected 0 but got { len( empty_list ) }"