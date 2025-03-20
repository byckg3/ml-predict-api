import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse, StreamingResponse

from app.api import router
from app.models.prompt import Prompt
from app.models.service.ai import GenerativeAIService

def ai_service( request: Request ) -> GenerativeAIService:

    if not hasattr( request.app.state, "ai_service" ):
        request.app.state.ai_service = GenerativeAIService()

    return request.app.state.ai_service

ServiceDependency = Annotated[ GenerativeAIService, Depends( ai_service ) ]

router = APIRouter( prefix = "/chat" )

@router.post( "/ask" )
async def answer_question( prompt: Prompt, service: ServiceDependency ):

    try:
        full_prompt = f"{ prompt.context }\n{ prompt.user_question }" 
        print( full_prompt )
        return service.answer( full_prompt )
    
    except Exception as e:
            print( e )
            print( traceback.format_exc() ) 

    return JSONResponse( content = { "message": "An error occurred" }, 
                         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR )

@router.post( "/ask_stream", response_class = StreamingResponse )
async def stream_answer( prompt: Prompt, service: ServiceDependency ):

    try:
        full_prompt = f"{ prompt.context }\n{ prompt.user_question }" 
        print( full_prompt )
    
        return StreamingResponse( service.stream_answer( full_prompt ), media_type = "text/event-stream" )
    
    except Exception as e:
            print( e )
            print( traceback.format_exc() ) 

    return JSONResponse( content = { "message": "An error occurred" }, 
                         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR )
    