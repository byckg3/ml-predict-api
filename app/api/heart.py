import traceback
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from app.models.dataset import MedicalRecord
from app.models.service import RecordService

def get_record_service( request: Request ) -> RecordService:
    return request.app.state.service

router = APIRouter( prefix="/heart" )

RecordServiceDependency = Annotated[ RecordService, Depends( get_record_service ) ]

@router.get( "/record/{id}" )
async def get_record( id: str, service: RecordServiceDependency ):
   
    try:
        record = await service.get_by_id( id )
        if record:
            return JSONResponse( content = record, status_code = status.HTTP_200_OK )      
    except Exception as e:
        print( e )
        print( traceback.format_exc() )
    
    return JSONResponse( content = { "message": f"Record {id} not found" }, 
                         status_code = status.HTTP_404_NOT_FOUND )
    
@router.post( "/record" )
async def save_record( record: dict[ str, Any ], service: RecordServiceDependency ):
    
    if await service.record_exists( record.get( "_id" ) ):
        raise HTTPException( status_code = status.HTTP_409_CONFLICT,
                             detail = f"Record {record[ '_id' ]} already exists" )
    try:
        new_record = await service.create( record )
        if new_record:
            return JSONResponse( content = new_record, 
                                 status_code = status.HTTP_201_CREATED )
    except Exception as e:
        print( e )
        print( traceback.format_exc() )
    
    return JSONResponse( content = { "message": "An error occurred" }, 
                         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR )

@router.put( "/record/{id}" )
async def put_record( id: str, patch: dict[ str, Any ], service: RecordServiceDependency ):
    
    try:
        matched, modified = await service.update_by_id( id, patch )

        if matched or modified:
            return JSONResponse( content = { "message": f"Record { id } updated successfully" }, 
                                 status_code = status.HTTP_200_OK )
    
    except Exception as e:
        print( e )
        print( traceback.format_exc() )
    
    return JSONResponse( content = { "message": f"Record { id } not found" }, 
                         status_code = status.HTTP_404_NOT_FOUND )
        
@router.patch( "/record/{id}" )
async def update_record( id: str, patch: dict[ str, Any ], service: RecordServiceDependency ):
    return await put_record( id, patch, service )

@router.delete( "/record/{id}" )
async def delete_record( id, service: RecordServiceDependency ):
    
    try:
        deleted_count = await service.delete_by_id( id )
        if deleted_count:
            return Response( status_code = 204 )
        
    except Exception as e:
        print( e )
        print( traceback.format_exc() )
    
    return JSONResponse( content = { "message": f"Record { id } not found" }, 
                         status_code = status.HTTP_404_NOT_FOUND )
        
@router.post( "/predict" )
async def predict_target( record: HeartHealthMetrics ):

    try:
        print( record )
        record.age = 99
        record.target = 1
        
        return { "result": record }
    
    except Exception as e:
        print( e )
        return { "error": "An error occurred" }
    
    