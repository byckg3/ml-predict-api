import random
import traceback
from typing import Annotated, Any
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.responses import JSONResponse
from app.api.controller import DocumentController, RecordController
from app.api.dependencies import liver_record_service, predict_service
from app.models.liver import LiverDiseaseFeatures, LiverDiseaseRecord, example
from app.models.service.base import RecordService
from app.models.service.disease import DiseasePredictionService

ServiceDependency = Annotated[ RecordService, Depends( liver_record_service ) ]

router = APIRouter( prefix = "/disease/liver" )

@router.get( "/record/{id}" )
async def get_record( id: PydanticObjectId, service: ServiceDependency ) -> LiverDiseaseRecord:

    return await DocumentController.get_document( id, service )

@router.get( "/records/{user_id}" )
async def find_user_records( user_id: PydanticObjectId , service: ServiceDependency, page: int = 1, page_size: int = 10 ) -> list[ LiverDiseaseRecord ]:
    
    return await RecordController.find_user_records( user_id, service, page, page_size )

@router.get( "/records" )
async def get_all_records( service: ServiceDependency, page: int = 1, page_size: int = 10 ) -> list[ LiverDiseaseRecord ]:
    
    return await DocumentController.get_all_documents( service, page, page_size )

@router.post( "/record", status_code = status.HTTP_201_CREATED )
async def save_record( service: ServiceDependency, record: LiverDiseaseRecord ) -> LiverDiseaseRecord:
    
    return await DocumentController.save_document( record, service )

@router.put( "/record/{id}" )
async def put_record( id: PydanticObjectId, service: ServiceDependency, 
                      patch: dict[ str, Any ] = Body( examples = [ example[ "updated_value1" ] ] ) ) -> LiverDiseaseRecord:

    return await DocumentController.update_document( id, patch, service )

@router.patch( "/record/{id}" )
async def update_record( id: PydanticObjectId, service: ServiceDependency, 
                         patch: dict[ str, Any ] = Body( examples = [ example[ "updated_value2" ] ] ) ) -> LiverDiseaseRecord:

    return await put_record( id, service, patch )

@router.delete( "/record/{id}", status_code = status.HTTP_204_NO_CONTENT )
async def delete_record( id: PydanticObjectId, service: ServiceDependency ) -> None:

    return await DocumentController.delete_document( id, service )

@router.delete( "/records", status_code = status.HTTP_204_NO_CONTENT )
async def delete_all_records( service: ServiceDependency ) -> None:

    return await DocumentController.delete_all_document( service )

@router.post( "/predict" )
async def predict_target( record: LiverDiseaseRecord, service: DiseasePredictionService = Depends( predict_service ) ):

    try:
        # record.diagnosis = random.choice( [ 0, 1 ] )
        features: LiverDiseaseFeatures = record.features
        result = service.predict( features )
        print( result)
        features.set_target( result )
        
        return features
    
    except Exception as e:
        print( e )
        print( traceback.format_exc() )
        return JSONResponse( content = { "message": "An error occurred" }, 
                             status_code = status.HTTP_400_BAD_REQUEST )