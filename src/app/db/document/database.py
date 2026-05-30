from typing import Type, TypeVar

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import mongo_settings
from app.schemas.heart import HeartDiseaseRecord
from app.schemas.liver import LiverDiseaseRecord
from app.user.v1.schemas import UserProfile

D = TypeVar( "D", bound = Document )
class MongoDB:

    URI = mongo_settings().MONGO_URI
    DB_NAME = mongo_settings().DB_NAME

    def __init__( self ):
        self.client = AsyncIOMotorClient( MongoDB.URI )
        self.db = self.client[ MongoDB.DB_NAME ]
        
        print( "Created MongoDB connection successfully" )

    async def init( self, 
                    doc_types: list[ Type[ D ] ] | None = [ LiverDiseaseRecord, HeartDiseaseRecord, UserProfile ] ):
        
        if self.db is None:
            raise ValueError( "Database instance cannot be None" )
        
        await init_beanie( database = self.db,  # type: ignore
                           document_models = doc_types )
        
        print( "Initialized Beanie document models successfully" )

    async def ping_server( self ):
        # Send a ping to confirm a successful connection
        try:
            await self.client.admin.command( "ping" )
            print( "Pinged MongoDB server successfully" )

            return True

        except Exception as e:
            print( e )
            return False

    async def close( self ):
        self.client.close()
        print( "Closed MongoDB connection successfully" )


# python -m app.db.document.database
if __name__ == "__main__":
    pass    