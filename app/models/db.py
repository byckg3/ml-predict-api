import asyncio
import chromadb
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import chroma_settings, mongo_settings
from app.models.heart import HeartDiseaseRecord
from app.models.liver import LiverDiseaseRecord
from app.services.ai import GenAIEmbeddingFunction
from app.models.user import UserProfile

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

    COLLECTION_NAME = chroma_settings().CHROMADB_COLLECTION_NAME

    def __init__( self, path = chroma_settings().path ):
        self.path = path
        self.client = chromadb.PersistentClient( path = self.path )
        self.collection = self.client.get_collection( name = ChromaDB.COLLECTION_NAME,
                                                      embedding_function = GenAIEmbeddingFunction() )

    

# python app/models/mongo.py
if __name__ == "__main__":
    monogoDB = MongoDB()
    asyncio.run( monogoDB.ping_server() )
    asyncio.run( monogoDB.close() )