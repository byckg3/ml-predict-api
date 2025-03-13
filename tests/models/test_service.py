
import pytest
import pytest_asyncio
from app.models.heart import HeartDiseaseRecord
from app.models.db import MongoDB
from app.models.service import DocumentService

@pytest_asyncio.fixture( loop_scope = "module" )
async def setup_mongo():
    MongoDB.DB_NAME = "test"
    monogo = MongoDB()
    await monogo.init_beanie()

    yield

    await monogo.close()

@pytest_asyncio.fixture( loop_scope = "module" )
async def heart_record_service():
    heart_record_service = DocumentService( HeartDiseaseRecord )

    return heart_record_service

@pytest.mark.db
@pytest.mark.asyncio( loop_scope = "module" )
async def test_service_crud_operations( setup_mongo, heart_record_service ):

    record = {
        "age": 52,
        "sex": 1,
        "cp": 0,
        "trestbps": 125,
        "chol": 212,
        "fbs": 0,
        "restecg": 1,
        "thalach": 168,
        "exang": 0,
        "oldpeak": 1,
        "slope": 2,
        "ca": 2,
        "thal": 3
    }
    heart_record = HeartDiseaseRecord( **record )

    # save
    save_result = await heart_record_service.save( heart_record )
    # print( save_result )
    assert save_result.id is not None
    assert save_result.id == heart_record.id
    
    # update
    update_result = await heart_record_service.update_by_id( heart_record.id, { "age": 67, "target": 1 } )
    # print( update_result )
    assert update_result.age == 67
    assert update_result.target == 1

     # get
    get_result = await heart_record_service.get_by_id( heart_record.id )
    assert get_result.id is not None
    assert get_result.id == heart_record.id

    # delete
    delete_result = await heart_record_service.delete_by_id( heart_record.id )
    # print( delete_result )
    assert delete_result.deleted_count == 1

    # get empty
    get_empty_result = await heart_record_service.get_by_id( heart_record.id )
    assert get_empty_result is None