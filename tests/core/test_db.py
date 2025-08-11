import shutil
import time
import pytest
from app.core.db import ChromaDB

from app.services.genai import GenAIEmbeddingFunction

@pytest.mark.db
class TestChromaDB:

    TEST_PATH = "./test_chroma"
    TEST_COLLECTION = "test"
    DATA_SIZE = 1

    @pytest.fixture
    def chroma( self ):
        chroma = ChromaDB( self.TEST_PATH, self.TEST_COLLECTION, GenAIEmbeddingFunction(), False )

        yield chroma

        chroma.client.delete_collection( self.TEST_COLLECTION )
        del chroma.client

    def test_find_documents( self, chroma ):
        
        chroma.load( n_records = self.DATA_SIZE )
        result = chroma.collection.get( limit = self.DATA_SIZE )
        # print( result )
        assert result[ "documents" ][ 0 ] is not None, "Failed to get data from ChromaDB"

    # def teardown_method( self, test_find_qas ):
    #     shutil.rmtree( self.TEST_PATH )