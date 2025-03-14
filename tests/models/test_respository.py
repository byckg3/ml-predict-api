import pytest
import pytest_asyncio
from app.models.liver import LiverDiseaseRecord
from app.models.db import MongoDB
from app.models.repository import DocumentRepository

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
class TestDocumentRepository:

    repository = DocumentRepository( LiverDiseaseRecord )

    def setup_method( self, method ):
        pass
        
    def teardown_method( self, method ):
        pass

    async def test_document_crud_operations( self, setup_mongo, liver_disease_record ):
    
        # save
        saved_document = await self.repository.save( liver_disease_record )

        assert saved_document.id is not None

        # update
        updated_document = await self.repository.update_by_id( saved_document.id, 
                                                          { "age": 67, "smoking": 1 } )
    
        assert updated_document.age == 67
        assert updated_document.smoking == 1

        # get
        get_result = await self.repository.get_by_id( saved_document.id )
    
        assert get_result.id is not None
        assert get_result.id == saved_document.id

        # delete
        deleted_count = await self.repository.delete_by_id( saved_document.id )
        assert deleted_count == 1

        # get empty
        empty_result = await self.repository.get_by_id( saved_document.id )
        assert empty_result is None

    @pytest.mark.asyncio( loop_scope = "module" )
    async def test_service_delete_all_documents( self, setup_mongo, liver_disease_record ):

        deleted_count = await self.repository.delete_all()
        assert deleted_count >= 0, f"failed: Expected >= 0 but got { deleted_count }"

        empty_list = await self.repository.find_all()
        assert len( empty_list ) == 0, f"failed: Expected 0 but got { len( empty_list ) }"
