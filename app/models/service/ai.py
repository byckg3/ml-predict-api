from fastapi import WebSocket
from google import genai
from google.genai import types

from app.config.settings import gemini_settings
from app.models.prompt import HealthCareDomain

class GenerativeAIService:
    
    API_KEY = gemini_settings().GEMINI_API_KEY
    MODEL = "gemini-2.0-flash" #  os.getenv( "TUNED_MODEL_ID" )
    
    client = genai.Client( api_key = API_KEY )
    
    def __init__( self, domain = HealthCareDomain ):
        self.content_config = types.GenerateContentConfig( 
                                        system_instruction = domain.context )
    
    def answer( self, question ):
        response = GenerativeAIService.client.models.generate_content(
                                                        model = GenerativeAIService.MODEL,
                                                        contents = [ question ] )
        return response.text
    
    def stream_answer( self, qa_records ):
        response = GenerativeAIService.client.models.generate_content_stream( 
                                                        model = GenerativeAIService.MODEL,
                                                        config = self.content_config,
                                                        contents = qa_records )
                                        
        for chunk in response:
            yield chunk.text

    @classmethod
    def create_chat( cls, domain = HealthCareDomain ):

        content_config = types.GenerateContentConfig( system_instruction = domain.context )
        chat = cls.client.chats.create( model = cls.MODEL,
                                        config = content_config )
        
        return chat

    def embeddings( cls, contents ):
        result = cls.client.models.embed_content( model = "gemini-embedding-exp-03-07",
                                                  contents = contents )
       
        return result.embeddings
    
class ChatSession:

    def __init__( self, chat, ws: WebSocket ):
        self.chat = chat
        self.websocket = ws

class WSChatManager:

    def __init__( self ):
        self.active_sessions: dict[ str, ChatSession ] = {}

    async def connect( self, user_id: str, websocket: WebSocket ):
        
        if user_id not in self.active_sessions:
            await websocket.accept()
           
            chat = GenerativeAIService.create_chat()
            session = ChatSession( chat, websocket )

            self.active_sessions[ user_id ] = session

        return self.active_sessions[ user_id ]


    def disconnect( self,  user_id: str, websocket: WebSocket ):

        websocket.close()
        if user_id in self.active_sessions:
            del self.active_sessions[ user_id ]
        
    async def send_user_message( self, user_id: str, message: str ):

        session = self.active_sessions[ user_id ]
        await session.websocket.send_text( message )

    async def broadcast( self, message: str ):

        for session in self.active_sessions:
            await session.websocket.send_text( message )