import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse, StreamingResponse
from app.api import router
from app.api.dependencies.service import chat_service, chat_manager
from app.llm.gemini.services import ChatService
from app.schemas.chat import ChatPayload
from app.services.genai import ChatManager

router = APIRouter( prefix = "/chat" )

ServiceDependency = Annotated[ ChatService, Depends( chat_service ) ]

@router.get( "/" )
async def websocket_info():
    """WebSocket endpoint is available, please visit `ws://{Host}/chat/{user_id}`"""
    return { "message": "websocket endpoint is available at ws://{Host}/chat/{user_id}" }


@router.post( "/ask", response_class = StreamingResponse )
async def streaming_answer( qa: ChatPayload, service: ServiceDependency ):

    try:
        text_generator = service.streaming_answer( qa )
        
        return StreamingResponse( text_generator, 
                                  media_type = "text/event-stream" )
       
    except Exception as e:
        print( e )
        print( traceback.format_exc() ) 

    return JSONResponse( content = { "message": "An error occurred" }, 
                         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR )
    

ChatManagerDependency = Annotated[ ChatManager, Depends( chat_manager ) ]

@router.websocket( "/{user_id}" )
async def websocket_endpoint( user_id: str, 
                              websocket: WebSocket, 
                              chat_manager: ChatManagerDependency ):
    
    user_session = await chat_manager.connect( user_id, websocket )
    chatbot = user_session.chat

    print( f"{user_id} connectting..." )
    try:
        response = chatbot.send_message( "使用者想詢問問題 請先親切地打招呼" )
        await websocket.send_text( response.text )

        while True:
            question = await websocket.receive_text()

            prompt = chat_manager.genai_service._augment_input( question )
            # print( prompt )
            response = chatbot.send_message( prompt )
            
            await websocket.send_text( response.text )
           
    # except WebSocketDisconnect:
    except Exception as e:
        print( e )
        print( traceback.format_exc() )

    await chat_manager.disconnect( user_id, websocket )