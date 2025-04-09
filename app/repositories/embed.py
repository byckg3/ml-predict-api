from app.core.config import chroma_settings
from app.core.db import ChromaDB


class ChromaRepository:

    DB_PATH = chroma_settings().CHROMA_DB_DIR
    COLLECTION_NAME = chroma_settings().CHROMA_DB_COLLECTION

    def __init__( self, path = DB_PATH, name = COLLECTION_NAME, function = None ):
        self.embed_db = ChromaDB( path, name, function )
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