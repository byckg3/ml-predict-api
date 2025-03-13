import traceback
from typing import Any
from beanie import Document
from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.models.service import DocumentService


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
    async def save_document( cls, doc: Document, service: DocumentService ):
    
        try:
            if await service.document_exists( getattr( doc, "id", None ) ):
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
                return JSONResponse( content = { "message": f"Document updated successfully" }, 
                                     status_code = status.HTTP_200_OK )
        except Exception as e:
            print( e )
            print( traceback.format_exc() )
        
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

