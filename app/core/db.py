import chromadb
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import chroma_settings, mongo_settings
from app.schemas.heart import HeartDiseaseRecord
from app.schemas.liver import LiverDiseaseRecord
from app.schemas.user import UserProfile
from app.services.ai import GenAIEmbeddingFunction

class MongoDB:

    URI = mongo_settings().MONGO_URI
    DB_NAME = mongo_settings().DB_NAME

    def __init__( self ):
        self.client = AsyncIOMotorClient( MongoDB.URI )
        self.db = self.client[ MongoDB.DB_NAME ]
        
        print( "create db connection successfully" )

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

    COLLECTION_NAME = chroma_settings().CHROMA_DB_COLLECTION

    def __init__( self, path = chroma_settings().CHROMA_DB_DIR ):
        self.path = path
        self.client = chromadb.PersistentClient( path = self.path )
        self.collection = self.client.get_collection( name = ChromaDB.COLLECTION_NAME,
                                                      embedding_function = GenAIEmbeddingFunction() )

    

# python -m app.schemas.db
if __name__ == "__main__":
    chroma = ChromaDB()
    print( chroma.collection.get( limit = 1 ) )
    