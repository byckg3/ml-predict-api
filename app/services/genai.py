from fastapi import WebSocket
from app.llm.gemini.service import ChatService
from app.services.disease import DiseasePredictionService

class ChatSession:

    def __init__( self, chat, ws: WebSocket ):
        self.chat = chat
        self.websocket = ws

class ChatManager:

    def __init__( self ):
        self.active_sessions: dict[ str, ChatSession ] = {}
        self.genai_service = ChatService( DiseasePredictionService())

    async def connect( self, user_id: str, websocket: WebSocket ):
        
        if user_id not in self.active_sessions:
            await websocket.accept()
           
            chat = self.genai_service.open_chat_session()
            session = ChatSession( chat, websocket )

            self.active_sessions[ user_id ] = session

        return self.active_sessions[ user_id ]


    async def disconnect( self,  user_id: str, websocket: WebSocket ):

        await websocket.close()
        if user_id in self.active_sessions:
            del self.active_sessions[ user_id ]
        
    async def send_user_message( self, user_id: str, message: str ):

        session = self.active_sessions[ user_id ]
        await session.websocket.send_text( message )

    async def broadcast( self, message: str ):

        for session in self.active_sessions.values():
            await session.websocket.send_text( message )