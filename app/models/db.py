import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

if os.path.exists( ".env" ):
    from dotenv import load_dotenv
    load_dotenv()

class MongoDB:

    URI = os.getenv( "MONGO_URI" )
    DB_NAME = os.getenv( "DB_NAME" )

    def __init__( self ):
        self.client = AsyncIOMotorClient( MongoDB.URI )
        self.db = self.client[ MongoDB.DB_NAME ]
        
        print( "create db connection successfully" )

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

# python app/models/mongo.py
if __name__ == "__main__":
    monogoDB = MongoDB()
    asyncio.run( monogoDB.ping_server() )
    asyncio.run( monogoDB.close() )
    
