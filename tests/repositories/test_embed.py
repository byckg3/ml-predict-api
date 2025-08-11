import pytest
from app.repositories.embed import ChromaRepository
from app.services.genai import GenAIEmbeddingFunction

# @pytest.mark.current
class TestChromaRepository:

    repository = ChromaRepository( function = GenAIEmbeddingFunction() )

    def test_find_qas( self ):
        num_results = 1
        contents = [ "你們有什麼服務" ]

        results = self.repository.find_qa_texts( contents, num_results )
        # print( results)
        assert len( results) == num_results
        assert all( isinstance( doc, str ) for doc in results )

    def test_find_documents( self ):
        num_results = 2
        contents = [ "如何降低心血管疾病風險" ]

        results = self.repository.find_pdf_documents( contents, num_results )
        # print( results)
        assert len( results) == num_results
        assert all( isinstance( doc, str ) for doc in results )