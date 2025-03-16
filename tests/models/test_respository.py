import pytest
import pytest_asyncio
from app.models.liver import LiverDiseaseRecord, example
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
    liver_disease_record = LiverDiseaseRecord( **example[ "created_record" ] )

    return liver_disease_record

@pytest.mark.db
@pytest.mark.asyncio( loop_scope = "module" )
class TestDocumentRepository:

    repository = DocumentRepository( LiverDiseaseRecord )

    def setup_method( self, method ):
        pass
        
    def teardown_method( self, method ):
        pass

    async def test_repository_crud_operations( self, setup_mongo, liver_disease_record ):
    
        # save
        saved_document = await self.repository.save( liver_disease_record )

        assert saved_document.id is not None

        # update
        updated_document = await self.repository.update_by_id( saved_document.id, 
                                                               example[ "updated_value1" ] )
    
        assert updated_document.features.alcohol_consumption == 18.2
        assert updated_document.features.smoking == 1

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
