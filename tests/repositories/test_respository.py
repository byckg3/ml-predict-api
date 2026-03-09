from pathlib import Path
import shutil
import pytest

from app.schemas.liver import LiverDiseaseRecord, example
from app.core.db import MongoDB
from app.repositories.nosql import DocumentRepository
from app.repositories.models import HFModelRepository

# @pytest.mark.test_only
@pytest.mark.usefixtures( "setup_mongo" )
class TestDocumentRepository:

    def setup_method( self, method ):
        pass
        
    def teardown_method( self, method ):
        pass
    
    
    @pytest.fixture( scope = "class" )
    def record_repository( self ):
        return DocumentRepository( LiverDiseaseRecord )

    @pytest.fixture( scope = "class" )
    async def liver_disease_record( self ):

        liver_disease_record = LiverDiseaseRecord( **example[ "created_record" ] )

        return liver_disease_record
    

    async def test_repository_crud_operations( self, record_repository, liver_disease_record ):
    
        # save
        saved_document = await record_repository.save( liver_disease_record )

        assert saved_document.id is not None

        # update
        updated_document = await record_repository.update_by_id( saved_document.id, 
                                                               example[ "updated_value1" ] )
    
        assert updated_document is not None
        assert updated_document.features.alcohol_consumption == 18.2
        assert updated_document.features.smoking == 1

        # get
        get_result = await record_repository.get_by_id( str( saved_document.id ) )
    
        assert get_result is not None
        assert get_result.id is not None
        assert get_result.id == saved_document.id

        # delete
        deleted_count = await record_repository.delete_by_id( saved_document.id )
        assert deleted_count == 1

        # get empty
        empty_result = await record_repository.get_by_id( str( saved_document.id ) )
        assert empty_result is None


    async def test_service_delete_all_documents( self, record_repository, liver_disease_record ):

        deleted_count = await record_repository.delete_all()
        assert deleted_count >= 0, f"failed: Expected >= 0 but got { deleted_count }"

        empty_list = await record_repository.find_all()
        assert len( empty_list ) == 0, f"failed: Expected 0 but got { len( empty_list ) }"


@pytest.mark.hf
class TestHFModelRepository:

    download_dir = "./temp"
    
    @pytest.fixture( scope = "class" )
    def hf_repository( self ):
        return HFModelRepository()

    async def test_repository_download_successfully( self, hf_repository: HFModelRepository ):
        
        repo_filepath = "liver/sklearn/random_forest/01/input_example.json"

        local_filepath = await hf_repository.download( repo_filepath, self.download_dir )
        file_path = Path( local_filepath )
        
        assert file_path.exists() == True, f"failed: Expected {file_path} exists"

    def teardown_method( self, test_repository_download_successfully ):
        shutil.rmtree( self.download_dir )