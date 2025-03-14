from typing import Any, TypeVar, Union
from beanie import Document, PydanticObjectId
from beanie.operators import In

from app.models.heart import HeartDiseaseRecord
from app.models.liver import LiverDiseaseRecord

T = TypeVar( "T", bound = Document )
class DocumentService:

    def __init__( self, document_class: T ):
        self.model_class = document_class
        
    async def get_by_id( self, id: str ) -> Union[ T, None ]:
        return await self.model_class.get( id )
    
    async def find_by_criteria( self, search_criteria: Any, skip = 0, limit = 10 ) -> list[ T ]:
    
        find_result = self.model_class.find( search_criteria )
        documents = await find_result.skip( skip ).limit( limit ).to_list()

        return documents
    
    async def find_all( self, skip = 0, limit = 10 ) -> list[ T ]:
    
        documents = await self.find_by_criteria( {}, skip, limit )

        return documents
    
    async def save( self, doc: T ) -> T:
        document = await doc.save()
        
        return document
    
    async def update_by_id( self, id, patch ) -> T:
        result = None

        doc = await self.get_by_id( id )
        if doc:
            result = await doc.update( { "$set": patch } )

        return result
    
    async def delete_by_id( self, id ) -> int:
        result, deleted_count = None, 0

        doc = await self.get_by_id( id )
        if doc:
            result = await doc.delete()
        
        if result:
            deleted_count = result.deleted_count
        
        return deleted_count
    
    async def delete_all( self ) -> int:
        deleted_count = 0

        result = await self.model_class.delete_all()
        if result:
            deleted_count = result.deleted_count
        
        return deleted_count
    
    async def id_exists( self, id ) -> bool:
        record = await self.get_by_id( id )
        if record:
            return True
        else:
            return False
        
U = TypeVar( "U", LiverDiseaseRecord, HeartDiseaseRecord )
class RecordService( DocumentService ):

    def __init__( self, record_class: U ):
        super().__init__( record_class )

    async def find_by_user_id( self, user_id: Union[ str, PydanticObjectId ], skip = 0, limit = 10 ):
        
        find_result = self.model_class.find( self.model_class.user_id == PydanticObjectId( user_id ) )
        records = await find_result.skip( skip ).limit( limit ).to_list()

        return records