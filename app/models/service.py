from typing import TypeVar
from beanie import Document

T = TypeVar( "T", bound = Document )
class DocumentService:

    def __init__( self, document_class: T ):
        self.model_class = document_class
        
    async def get_by_id( self, id ):
        return await self.model_class.get( id )
    
    async def save( self, doc: T ):
        await doc.save()
        return doc
    
    async def update_by_id( self, id, patch ):
        result = None

        doc = await self.get_by_id( id )
        if doc:
            result = await doc.update( { "$set": patch } )

        return result
    
    async def delete_by_id( self, id ):
        result = None

        doc = await self.get_by_id( id )
        if doc:
            result = await doc.delete()
        
        return result 
    
    async def document_exists( self, id ):
        record = await self.get_by_id( id )
        if record:
            return True
        else:
            return False