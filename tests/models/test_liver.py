import pytest
import pytest_asyncio
from app.models.liver import LiverDiseaseRecord
from app.models.db import MongoDB

@pytest_asyncio.fixture( loop_scope = "module" )
async def setup_mongo():
    MongoDB.DB_NAME = "test"
    monogo = MongoDB()
    await monogo.init_beanie()

    yield

    await monogo.close()

@pytest_asyncio.fixture( loop_scope = "module" )
async def liver_disease_record():
    record = {  "age": 58,
                "gender": 0,
                "bmi": 35.8,
                "alcohol_consumption": 17.2,
                "smoking": 0,
                "genetic_risk": 1,
                "physical_activity": 0.658,
                "diabetes": 0,
                "hypertension": 0,
                "liver_function_test": 42.73,
                "diagnosis": 1 }
    liver_disease_record = LiverDiseaseRecord( **record )

    return liver_disease_record

@pytest.mark.db
@pytest.mark.asyncio( loop_scope = "module" )
class TestLiverDiseaseRecord:

    def setup_method( self, method ):
        pass
        
    def teardown_method( self, method ):
        pass

    async def test_document_crud_operations( self, setup_mongo, liver_disease_record ):
       
        # save
        save_result = await liver_disease_record.save()

        assert save_result.id is not None
        assert save_result.id == liver_disease_record.id

        # update
        update_result = await liver_disease_record.update( { "$set": { "age": 67, "smoking": 1 } } )
    
        assert update_result.age == 67
        assert update_result.smoking == 1

        # get
        get_result = await LiverDiseaseRecord.get( liver_disease_record.id )
    
        assert get_result.id is not None
        assert get_result.id == liver_disease_record.id

        # delete
        delete_result = await liver_disease_record.delete()

        assert delete_result.deleted_count == 1

        # get empty
        get_empty_result = await LiverDiseaseRecord.get( liver_disease_record.id )
        assert get_empty_result is None

    @pytest.mark.asyncio( loop_scope = "module" )
    async def test_service_delete_all_documents( self, setup_mongo, liver_disease_record ):

        deleted_redult = await liver_disease_record.delete_all()
        assert deleted_redult.deleted_count >= 0, f"failed: Expected >= 0 but got { deleted_redult.deleted_count }"

        empty_list = await liver_disease_record.find( {} ).to_list()
        assert len( empty_list ) == 0, f"failed: Expected 0 but got { len( empty_list ) }"
