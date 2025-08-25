from typing import Any
from chromadb import Documents, EmbeddingFunction, Embeddings
from fastapi import WebSocket
from google import genai
from google.genai import types

from app.core.config import gemini_settings
from app.repositories.embed import ChromaRepository
from app.schemas.prompt import HealthCare

class GenerativeAIService:
    
    API_KEY = gemini_settings().GEMINI_API_KEY
    MODEL = "gemini-2.0-flash" #  os.getenv( "TUNED_MODEL_ID" )
    
    client = genai.Client( api_key = API_KEY )
    
    def __init__( self, domain = HealthCare ):
        self.domain = domain
        self.embed_repository = ChromaRepository( function = GenAIEmbeddingFunction( self.API_KEY ) )
        self.content_config = types.GenerateContentConfig( 
                                        system_instruction = self.domain.system_prompt )
        
    
    def answer( self, question ):
        response = GenerativeAIService.client.models.generate_content(
                                                        model = GenerativeAIService.MODEL,
                                                        contents = [ question ] )
        return response.text
    
    def streaming_answer( self, qa_records ):
        response = GenerativeAIService.client.models.generate_content_stream( 
                                                        model = GenerativeAIService.MODEL,
                                                        config = self.content_config,
                                                        contents = qa_records )
                                        
        for chunk in response:
            yield chunk.text

    def rag_prompt( self, question ):
        qas = self.embed_repository.find_qa_texts( question )
        docs = self.embed_repository.find_pdf_documents( question )

        input = {
            "retrieved_content": "\n".join( qas ),
            "retrieved_document": "\n".join( docs ),
            "user_query": question
        }
        prompt = HealthCare.chat_template.format( **input )

        return prompt
    
    # https://ai.google.dev/api/caching?hl=zh-tw#Content
    def add_chat_history( self, past_messages ):

        past = []
        for msg in past_messages:
            
            payload = { "role": "", "parts": [] }
            if msg[ "role" ] == "user":
                payload[ "role" ] = "user"

            else:
                payload[ "role" ] = "model"

            payload[ "parts" ].append( { "text": msg[ "content" ] } )
            past.append( payload )
            
        return past

    @classmethod
    def create_chat( cls, domain = HealthCare ):

        content_config = types.GenerateContentConfig( system_instruction = domain.system_prompt )
        chat = cls.client.chats.create( model = cls.MODEL,
                                        config = content_config )
        
        return chat
    
class ChatSession:

    def __init__( self, chat, ws: WebSocket ):
        self.chat = chat
        self.websocket = ws

class ChatManager:

    def __init__( self ):
        self.active_sessions: dict[ str, ChatSession ] = {}
        self.genai_service = GenerativeAIService()

    async def connect( self, user_id: str, websocket: WebSocket ):
        
        if user_id not in self.active_sessions:
            await websocket.accept()
           
            chat = self.genai_service.create_chat()
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

class GenAIEmbeddingFunction( EmbeddingFunction[ Documents ] ):

    def __init__( self, api_key: str = None, 
                  model_name: str = "gemini-embedding-exp-03-07", 
                  task_type = "SEMANTIC_SIMILARITY" ) -> None:
        
        if api_key is None:
            api_key = gemini_settings().GEMINI_API_KEY

        self.api_key = api_key  
        self.client = genai.Client( api_key = self.api_key )
        self.model_name = model_name
        self.task_type = task_type

    def __call__( self, input: Documents ) -> Embeddings:
       
        result = self.client.models.embed_content( model = self.model_name,
                                                   contents = input,
                                                   config = types.EmbedContentConfig( task_type = self.task_type )
                                    )
       
        return [ embedding.values for embedding in result.embeddings ]
    
    @staticmethod
    def name() -> str:
        return "GenAIEmbeddingFunction"
    
    def get_config(self) -> dict[ str, Any ]:
        pass

    @staticmethod
    def build_from_config(config: dict[ str, Any ]) -> "EmbeddingFunction[D]":
        pass