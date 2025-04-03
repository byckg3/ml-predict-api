import chromadb
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

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

    def __init__( self, path: str, name: str, embed_function = None ):
        self.client = chromadb.PersistentClient( path )
        self.collection = self.client.get_or_create_collection( name = name,
                                                                embedding_function = embed_function )

    def load( self, dataset = [], embeddings = [] ):

        if self.ping():
            print( "data loaded successfully" )
        else:
            print( "data loading failed" )
        
    
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
    chroma = ChromaDB()
    print( chroma.collection.get( limit = 1 ) )
    