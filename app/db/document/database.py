from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import mongo_settings
from app.schemas.heart import HeartDiseaseRecord
from app.schemas.liver import LiverDiseaseRecord
from app.schemas.user import UserProfile

class MongoDB:

    URI = mongo_settings().MONGO_URI
    DB_NAME = mongo_settings().DB_NAME

    def __init__( self ):
        self.client = AsyncIOMotorClient( MongoDB.URI )
        self.db = self.client[ MongoDB.DB_NAME ]
        
        print( "create MonogoDb connection successfully" )

    async def init_beanie( self ):
        
        if self.db is None:
            raise ValueError( "database instance cannot be None" )
        
        await init_beanie( database = self.db,  # type: ignore
                           document_models = [ LiverDiseaseRecord, HeartDiseaseRecord, UserProfile ] )

        print( "initialize Beanie successfully" )

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


# python -m app.core.db
if __name__ == "__main__":
    pass    