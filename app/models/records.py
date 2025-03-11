import asyncio
from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


class RecordRepository:

    COLLECTION_NAME = "heart-records"

    def __init__( self, db ):
        self.records = db[ RecordRepository.COLLECTION_NAME ]
        print( "create record repository successfully" )

    async def find_one( self, id ):
        record = await self.records.find_one( { "_id": ObjectId( id ) } )

        if record:
            record[ "_id" ] = str( record[ "_id" ] )
            
        return record

    async def insert_one( self, new_record ):
        result = None
        try:
            result = await self.records.insert_one( new_record )
            # The document to insert. If the document does not have an _id field one will be added automatically.
            new_record[ "_id" ] = str( new_record[ "_id" ] )

            return str( result.inserted_id )
        
        except Exception as e:
            print( e )

        return result
    
    async def update_one( self, id, patch ):
        result = await self.records.update_one( { "_id": ObjectId( id ) }, { "$set": patch } )

        return result.matched_count, result.modified_count
        
    async def delete_one( self, id ):
        result = await self.records.delete_one( { "_id": ObjectId( id ) } )
         
        return result.deleted_count

# python app/models/records.py
if __name__ == "__main__":
    repo = RecordRepository()
    new_record =  { "age": 45,
                    "sex": 1,
                    "cp": 3,
                    "trestbps": 120,
                    "chol": 233,
                    "fbs": 0,
                    "restecg": 1,
                    "thalach": 170,
                    "exang": 0,
                    "oldpeak": 2.3,
                    "slope": 2,
                    "ca": 0,
                    "thal": 2,
                    "target": 0 }
    
    # inserted_id = asyncio.run( repo.insert_one( new_record ) )
    # print( inserted_id )
    # modified_count = asyncio.run( repo.update_one( "67ceb3cf486f0e96a7c0ac25", { "target": 1 } ) )
    # print( modified_count )
    # record = asyncio.run( repo.find_one( "67ce5b0baae4a4c83782d2bd" ) )
    # print( record )
    # deleted_count = asyncio.run( repo.delete_one( "67ce5b0baae4a4c83782d2bd" ) )
    # print( deleted_count )