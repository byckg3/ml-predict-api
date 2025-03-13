import random
import traceback
from typing import Annotated, Any
from fastapi import APIRouter, Body, Depends, Request
from app.api.controller import DocumentController
from app.models.heart import HeartDiseaseRecord
from app.models.service import DocumentService

def heart_record_service( request: Request ) -> DocumentService:

    heart_record_service = None
    if hasattr( request.app.state, "heart_record_service" ):
        heart_record_service = request.app.state.heart_record_service
    else:
        heart_record_service = DocumentService( HeartDiseaseRecord )
        request.app.state.heart_record_service = heart_record_service

    return heart_record_service

ServiceDependency = Annotated[ DocumentService, Depends( heart_record_service ) ]

router = APIRouter( prefix="/heart" )

@router.get( "/record/{id}" )
async def get_record( id: str, service: ServiceDependency ) -> HeartDiseaseRecord:

    return await DocumentController.get_document( id, service )
    
@router.post( "/record" )
async def save_record( record: HeartDiseaseRecord, service: ServiceDependency ):
    
    return await DocumentController.save_document( record, service )

@router.put( "/record/{id}" )
async def put_record( id: str, service: ServiceDependency, 
                      patch: dict[ str, Any ] = Body( ..., example = { "trestbps": 125, "target": 0 } ) ):

    return await DocumentController.update_document( id, patch, service )
        
@router.patch( "/record/{id}" )
async def update_record( id: str, service: ServiceDependency, 
                         patch: dict[ str, Any ] = Body( ..., example = { "chol": 212, "thalach": 168 } ) ):

    return await put_record( id, patch, service )

@router.delete( "/record/{id}" )
async def delete_record( id, service: ServiceDependency ):

    return await DocumentController.delete_document( id, service )
        
@router.post( "/predict" )
async def predict_target( record: HeartDiseaseRecord ):

    try:
        record.target = random.choice( [ 0, 1 ] )
        
        return { "result": record }
    
    except Exception as e:
        print( e )
        print( traceback.format_exc() )
        return { "error": "An error occurred" }
    
    