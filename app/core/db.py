import chromadb
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd

from app.core.config import chroma_settings, mongo_settings
from app.schemas.heart import HeartDiseaseRecord
from app.schemas.liver import LiverDiseaseRecord
from app.schemas.user import UserProfile

class MongoDB:

    URI = mongo_settings().MONGO_URI
    DB_NAME = mongo_settings().DB_NAME

    def __init__( self ):
        self.client = AsyncIOMotorClient( MongoDB.URI )
        self.db = self.client[ MongoDB.DB_NAME ]
        
        print( "create monogodb connection successfully" )

    async def init_beanie( self ):
        await init_beanie( database = self.db, document_models = [ LiverDiseaseRecord, HeartDiseaseRecord, UserProfile ] )

        print( "initialize beanie successfully" )

    async def ping_server( self ):
        # Send a ping to confirm a successful connection
        try:
            await self.client.admin.command( 'ping' )
            print( "Pinged your deployment. You successfully connected to MongoDB!" )

            return True

        except Exception as e:
            print( e )
            return False

    async def close( self ):
        self.client.close()

class ChromaDB:

    def __init__( self, path: str, name: str, embed_function = None, is_persistent: bool = False ):

        if is_persistent:
            self.client = chromadb.PersistentClient( path )
        else:
            self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection( name = name,
                                                                embedding_function = embed_function )
        print( "create chroma db connection successfully" )

    def load( self, n_records = -1 ):

        qa_data_df = pd.read_parquet( "./data/qa.parquet", engine = "pyarrow" )
        heart_disease_df = pd.read_parquet( "./data/heart_disease.parquet", engine = "pyarrow" )
        liver_disease_df = pd.read_parquet( "./data/liver_disease.parquet", engine = "pyarrow" )

        self.add( qa_data_df, n_records )
        self.add( heart_disease_df, n_records )
        self.add( liver_disease_df, n_records )

        if self.ping():
            print( "data loaded successfully" )
        else:
            print( "data loading failed" )

    def add( self, df, n_records = -1 ):
        
        n = df.shape[ 0 ]
        if n_records >= 0:
            n = min( n, n_records )

        embeddings = df[ "embedding" ].tolist()[ :n ]
        documents = df[ "document" ].tolist()[ :n ]
        ids = df[ "id" ].tolist()[ :n ]
        metadatas = df.drop( columns = [ "id", "document", "embedding" ] ).to_dict( orient = "records" )[  :n ]

        self.collection.upsert(
                documents = documents,
                embeddings = embeddings,
                ids = ids,
                metadatas = metadatas,
        )
    
    def ping( self ):
        try:
            result = self.collection.get( limit = 1 )
            if result:
                return True
            
        except Exception as e:
            print( e )

        return False

# python -m app.core.db
if __name__ == "__main__":
    pass    