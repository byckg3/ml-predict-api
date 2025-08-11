from beanie import Document
from datetime import datetime, timezone
from typing import Any, TypeVar, Union

T = TypeVar( "T", bound = Document )
class DocumentRepository:

    def __init__( self, document_class: T ):

        self.beanie_document = document_class

    async def get_by_id( self, id: str ) -> Union[ T, None ]:
        return await self.beanie_document.get( id )
    
    async def find_by_criteria( self, search_criteria: Any, skip = 0, limit = 10 ) -> list[ T ]:
        find_result = self.beanie_document.find( search_criteria )
        documents = await find_result.skip( skip ).limit( limit ).to_list()

        return documents
    
    async def find_one( self, search_criteria: Any ) -> T:
        document = await  self.beanie_document.find_one( search_criteria )

        return document
    
    async def find_all( self, skip = 0, limit = 10 ) -> list[ T ]:
        documents = await self.find_by_criteria( {}, skip, limit )

        return documents
    
    async def save( self, document: T ) -> T:
        return await document.save() 
    
    async def update_by_id( self, id, patch ) -> T:
        result = None

        document = await self.get_by_id( id )
        if document:
            patch = patch | { "updated_at": datetime.now( timezone.utc ) }
            result = await document.update( { "$set": patch } )

        return result
    
    async def delete_by_id( self, id ) -> int:
        result, deleted_count = None, 0

        document = await self.get_by_id( id )
        if document:
            result = await document.delete()
        
        if result:
            deleted_count = result.deleted_count
        
        return deleted_count
    
    async def delete_all( self ) -> int:
        deleted_count = 0

        result = await self.beanie_document.delete_all()
        if result:
            deleted_count = result.deleted_count
        
        return deleted_count
    
    async def id_exists( self, id ) -> bool:
        document = await self.get_by_id( id )
        if document:
            return True
        else:
            return False