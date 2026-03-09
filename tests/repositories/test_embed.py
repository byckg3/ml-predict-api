import pytest
from app.llm.gemini.services import GeminiEmbeddingFunction
from app.repositories.embed import ChromaRepository

# @pytest.mark.test_only
class TestChromaRepository:

    @pytest.fixture( scope = "class" )
    def repository( self ):
        return ChromaRepository( function = GeminiEmbeddingFunction() )
    

    def test_find_qas( self, repository: ChromaRepository ):
        num_results = 1
        contents = [ "你們有什麼服務" ]

        results = repository.find_qa_texts( contents, num_results )
        # print( results)
        assert len( results) == num_results
        assert all( isinstance( doc, str ) for doc in results )

    def test_find_documents( self, repository: ChromaRepository ):
        num_results = 2
        contents = [ "如何降低心血管疾病風險" ]

        results = repository.find_pdf_documents( contents, num_results )
        # print( results)
        assert len( results) == num_results
        assert all( isinstance( doc, str ) for doc in results )