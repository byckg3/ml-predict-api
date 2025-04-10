from app.core.config import chroma_settings
from app.core.db import ChromaDB


class ChromaRepository:

    DB_PATH = chroma_settings().CHROMA_DB_DIR
    COLLECTION_NAME = chroma_settings().CHROMA_DB_COLLECTION
    DB_PERSISTENT = chroma_settings().CHROMA_DB_PERSISTENT

    def __init__( self, function = None ):
        self.embed_db = ChromaDB( self.DB_PATH, 
                                  self.COLLECTION_NAME, 
                                  function, 
                                  self.DB_PERSISTENT )
        self.collection = self.embed_db.collection
        self.embed_db.load() 
     
    def find_qa_texts( self, contents, n = 2 ):
        result = self.collection.query( query_texts = contents, 
                                        n_results = n,
                                        where = { "category": "qa" }
                                 )
        return result[ "documents" ][ 0 ]
    
    def find_pdf_documents( self, contents, n = 2 ):
        result = self.collection.query( query_texts = contents, 
                                        n_results = n,
                                        where = { "category": "pdf" }
                                 )
        return result[ "documents" ][ 0 ]