import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse, StreamingResponse

from app.api import router
from app.schemas.prompt import HealthCare, HealthCarePrompt
from app.services.genai import GenerativeAIService, ChatManager

def ai_service( request: Request ) -> GenerativeAIService:

    if not hasattr( request.app.state, "ai_service" ):
        request.app.state.ai_service = GenerativeAIService()

    return request.app.state.ai_service

chat_router = APIRouter( prefix = "/chat", tags = [ "Chat" ] )

ServiceDependency = Annotated[ GenerativeAIService, Depends( ai_service ) ]

@chat_router.post( "/ask", response_class = StreamingResponse )
async def streaming_answer( prompt: HealthCarePrompt, service: ServiceDependency ):

    try:
        full_prompt = f"{ prompt.user_question }" 
        print( full_prompt )
    
        return StreamingResponse( service.stream_answer( full_prompt ), media_type = "text/event-stream" )
        # return service.answer( full_prompt )
    
    except Exception as e:
            print( e )
            print( traceback.format_exc() ) 

    return JSONResponse( content = { "message": "An error occurred" }, 
                         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR )

@chat_router.get( "/" )
async def websocket_info():
    """WebSocket endpoint is available, please visit `ws://{Host}/chat/{user_id}`"""
    return { "message": "websocket endpoint is available at ws://{Host}/chat/{user_id}" }

chat_manager = ChatManager()

@chat_router.websocket( "/{user_id}" )
async def websocket_endpoint( user_id: str, websocket: WebSocket ):
    
    user_session = await chat_manager.connect( user_id, websocket )
    chatbot = user_session.chat

    print( f"{user_id} connectting..." )
    try:
        response = chatbot.send_message( "使用者想詢問問題 請先親切地打招呼" )
        await websocket.send_text( response.text )

        while True:
            question = await websocket.receive_text()

            prompt = chat_manager.genai_service.rag_prompt( question )
            # print( prompt )
            response = chatbot.send_message( prompt )
            
            await websocket.send_text( response.text )
           
    # except WebSocketDisconnect:
    except Exception as e:
        print( e )
        print( traceback.format_exc() )

    chat_manager.disconnect( user_id, websocket )