from app.models.records import RecordRepository

class RecordService:
    def __init__(self, record_repository: RecordRepository ):
        self.record_repository = record_repository
        print( "create record service successfully" )

    # def get_all(self):
    #     return self.record_repository.get_all()

    async def get_by_id( self, id ):
        record = None
        if id:
            record = await self.record_repository.find_one( id )

        return record
    
    async def record_exists( self, id ):
        record = await self.get_by_id( id )
        if record:
            return True
        else:
            return False

    async def create( self, record ):
        new_record = None
        new_id = None
        if "_id" not in record:
            new_id =  await self.record_repository.insert_one( record )
       
        if new_id:
            new_record = record
            new_record[ "_id" ] = new_id
        
        return new_record
            
    async def update_by_id( self, id, patch ):
        if await self.record_exists( id ):
            return await self.record_repository.update_one( id, patch )

    async def delete_by_id( self, id ):
        return await self.record_repository.delete_one( id )