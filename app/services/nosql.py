from typing import Any, TypeVar, Union
from beanie import Document, PydanticObjectId
from beanie.operators import In

from app.schemas.heart import HeartDiseaseRecord
from app.schemas.liver import LiverDiseaseRecord
from app.repositories.nosql import DocumentRepository

T = TypeVar( "T", bound = Document )
class DocumentService:

    def __init__( self, document_class: T ):
        self.repository = DocumentRepository( document_class )
        
    async def get_by_id( self, id: str ) -> Union[ T, None ]:
        return await self.repository.get_by_id( id )
      
    async def find_all( self, skip = 0, limit = 10 ) -> list[ T ]:
        return await self.repository.find_all( skip, limit )
    
    async def save( self, doc: T ) -> T:
        return await self.repository.save( doc )
    
    async def update_by_id( self, id, patch ) -> T:
        return await self.repository.update_by_id( id, patch )
    
    async def delete_by_id( self, id ) -> int:
        return await self.repository.delete_by_id( id )
    
    async def delete_all( self ) -> int:
        return await self.repository.delete_all()
    
    async def id_exists( self, id ) -> bool:
        return await self.repository.id_exists( id )
    
U = TypeVar( "U", LiverDiseaseRecord, HeartDiseaseRecord )
class RecordService( DocumentService ):

    def __init__( self, record_class: U ):
        super().__init__( record_class )
        self.record_class = record_class

    async def find_by_user_id( self, user_id: Union[ str, PydanticObjectId ], skip = 0, limit = 10 ): 
        return await self.repository.find_by_criteria( self.record_class.user_id == PydanticObjectId( user_id ), 
                                                       skip, 
                                                       limit )