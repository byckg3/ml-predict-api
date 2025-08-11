import traceback
from typing import Any
from beanie import Document
from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.services.nosql import DocumentService, RecordService

class DocumentController:
    
    @classmethod
    async def get_document( cls, id: str, service: DocumentService ):
    
        try:
            record = await service.get_by_id( id )
            if record:
                return JSONResponse( content = jsonable_encoder( record ), 
                                     status_code = status.HTTP_200_OK )     
        except Exception as e:
            print( e )
            print( traceback.format_exc() )
        
        return JSONResponse( content = { "message": f"Document not found" }, 
                             status_code = status.HTTP_404_NOT_FOUND )
    
    @classmethod
    async def get_all_documents( cls, service: DocumentService, page: int = 1, page_size: int = 10  ):
    
        skip_count = ( page - 1 ) * page_size
        limit_count = page_size
        try:
            records = await service.find_all( skip = skip_count, limit = limit_count  )
            
            return JSONResponse( content = jsonable_encoder( records ), 
                                 status_code = status.HTTP_200_OK )     
        except Exception as e:
            print( e )
            print( traceback.format_exc() )
            return JSONResponse( content = { "message": "An error occurred" }, 
                                 status_code = status.HTTP_400_BAD_REQUEST )
    
    @classmethod
    async def save_document( cls, doc: Document, service: DocumentService ):
    
        try:
            if await service.id_exists( getattr( doc, "id", None ) ):
                return JSONResponse( content = { "message": f"Document already exists" },
                                     status_code = status.HTTP_409_CONFLICT )

            new_record = await service.save( doc )
            if new_record:
                return JSONResponse( content = jsonable_encoder( new_record ), 
                                     status_code = status.HTTP_201_CREATED )
        except Exception as e:
            print( e )
            print( traceback.format_exc() )
        
        return JSONResponse( content = { "message": "An error occurred" }, 
                             status_code = status.HTTP_500_INTERNAL_SERVER_ERROR )
    
    @classmethod
    async def update_document( cls, id: str, patch: dict[ str, Any ], service: DocumentService ):
    
        try:
            updated = await service.update_by_id( id, patch )

            if updated:
                return JSONResponse( content = jsonable_encoder( updated ), 
                                     status_code = status.HTTP_200_OK )
        except Exception as e:
            print( e )
            print( traceback.format_exc() )
            return JSONResponse( content = { "message": "An error occurred" }, 
                                 status_code = status.HTTP_400_BAD_REQUEST )
        
        return JSONResponse( content = { "message": f"Document not found" }, 
                             status_code = status.HTTP_404_NOT_FOUND )
    
    @classmethod
    async def delete_document( cls, id: str, service: DocumentService ):
    
        try:
            deleted_count = await service.delete_by_id( id )
            if deleted_count:
                return Response( status_code = 204 )
            
        except Exception as e:
            print( e )
            print( traceback.format_exc() )
        
        return JSONResponse( content = { "message": f"Document not found" }, 
                             status_code = status.HTTP_404_NOT_FOUND )
    
    @classmethod
    async def delete_all_document( cls, service: DocumentService ):

        try:
            deleted_count = await service.delete_all()
            
            return Response( status_code = 204 )
            
        except Exception as e:
            print( e )
            print( traceback.format_exc() )
        
        return JSONResponse( content = { "message": "An error occurred" }, 
                             status_code = status.HTTP_500_INTERNAL_SERVER_ERROR )
    
    

class RecordController:

    @classmethod
    async def find_user_records( cls, user_id: str, service: RecordService, page: int = 1, page_size: int = 10  ):
    
        skip_count = ( page - 1 ) * page_size
        limit_count = page_size
        try:
            records = await service.find_by_user_id( user_id, skip = skip_count, limit = limit_count  )
            
            return JSONResponse( content = jsonable_encoder( records ), 
                                 status_code = status.HTTP_200_OK )     
        except Exception as e:
            print( e )
            print( traceback.format_exc() )

        return JSONResponse( content = { "message": "An error occurred" }, 
                             status_code = status.HTTP_400_BAD_REQUEST )