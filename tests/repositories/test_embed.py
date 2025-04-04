import pytest
from app.repositories.embed import ChromaRepository
from app.services.genai import GenAIEmbeddingFunction

# @pytest.mark.current
class TestChromaRepository:

    repository = ChromaRepository( function = GenAIEmbeddingFunction() )

    def test_find_qas( self ):
        num_results = 3
        contents = [ "你們有什麼服務" ]

        results = self.repository.find_qas( contents, num_results )
        # print( results)
        assert len( results) == num_results
        assert all( isinstance( doc, str ) for doc in results )