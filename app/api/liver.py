import random
import traceback
from typing import Annotated, Any
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.api.controller import DocumentController
from app.models.liver import LiverDiseaseRecord
from app.models.service import DocumentService, DocumentService

def liver_record_service( request: Request ) -> DocumentService:

    liver_record_service = None
    if hasattr( request.app.state, "liver_record_service" ):
        liver_record_service = request.app.state.liver_record_service
    else:
        liver_record_service = DocumentService( LiverDiseaseRecord )
        request.app.state.liver_record_service = liver_record_service

    return liver_record_service

ServiceDependency = Annotated[ DocumentService, Depends( liver_record_service ) ]

router = APIRouter( prefix="/liver" )

@router.get( "/record/{id}" )
async def get_record( id: str, service: ServiceDependency ) -> LiverDiseaseRecord:

    return await DocumentController.get_document( id, service )

@router.post( "/record" )
async def save_record( record: LiverDiseaseRecord, service: ServiceDependency ):
    
    return await DocumentController.save_document( record, service )

@router.put( "/record/{id}" )
async def put_record( id: str, service: ServiceDependency, 
                      patch: dict[ str, Any ] = Body( ..., example = { "physical_activity": 0.657, "bmi": 33.2 } ) ):

    return await DocumentController.update_document( id, patch, service )

@router.patch( "/record/{id}" )
async def update_record( id: str, service: ServiceDependency, 
                         patch: dict[ str, Any ] = Body( ..., example = { "age": 31, "diagnosis": 1 } ) ):

    return await put_record( id, patch, service )

@router.delete( "/record/{id}" )
async def delete_record( id, service: ServiceDependency ):

    return await DocumentController.delete_document( id, service )

@router.post( "/predict" )
async def predict( record: LiverDiseaseRecord ):

    try:
        record.diagnosis = random.choice( [ 0, 1 ] )
        
        return { "result": record }
    
    except Exception as e:
        print( e )
        print( traceback.format_exc() )
        return { "error": "An error occurred" }


def liver_record_example():
    lhm = { "age": 58,
            "gender": 0,
            "bmi": 35.8,
            "alcohol_consumption": 17.2,
            "smoking": 0,
            "genetic_risk": 1,
            "physical_activity": 0.658,
            "diabetes": 0,
            "hypertension": 0,
            "liver_function_test": 42.73,
            "diagnosis": 1 }
    return lhm