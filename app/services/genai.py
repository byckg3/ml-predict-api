from typing import Any
from chromadb import Documents, EmbeddingFunction, Embeddings
from fastapi import WebSocket
from google import genai
from google.genai import types

from app.core.config import gemini_settings
from app.core.llm import GeminiAPIClient
from app.repositories.embed import ChromaRepository
from app.schemas.prompt import HealthCare

class TextGenerationService:
    
    def __init__( self, domain = HealthCare ):
        self.domain = domain
        self.embed_repository = ChromaRepository( function = GenAIEmbeddingFunction() )
        self.client = GeminiAPIClient( self.domain.system_prompt )
        
    
    def answer( self, question ):
        response = self.client.generate_text( question )
        return response
    
    
    async def streaming_answer( self, qa_records ):
        text_generatror = self.client.generate_text_stream( qa_records )
                                        
        async for text_chunk in text_generatror:
            text_chunk = text_chunk or ""
            
            yield text_chunk
            

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

    def open_chat_session( self, domain = HealthCare ):
        return self.client.create_chat()
        
       
    
class ChatSession:

    def __init__( self, chat, ws: WebSocket ):
        self.chat = chat
        self.websocket = ws

class ChatManager:

    def __init__( self ):
        self.active_sessions: dict[ str, ChatSession ] = {}
        self.genai_service = TextGenerationService()

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

class GenAIEmbeddingFunction( EmbeddingFunction[ Documents ] ):
    
    API_KEY = gemini_settings().API_KEY
    DEFAULT_MODEL_NAME = gemini_settings().EMBEDDING_MODEL_NAME
    DEFAULT_TASK_TYPE = "RETRIEVAL_DOCUMENT"

    def __init__( self, api_key: str | None = None, 
                  model_name: str | None = None, 
                  task_type: str | None = None ) -> None:
        
        self.model_name = model_name if model_name else self.DEFAULT_MODEL_NAME
        self.task_type = task_type if task_type else self.DEFAULT_TASK_TYPE
        
        self.client = genai.Client( api_key = self.API_KEY )

    def __call__( self, input: Documents ) -> list[ list[ float ] ]:
       
        result = self.client.models.embed_content( 
            model = self.model_name,
            contents = input,
            config = types.EmbedContentConfig( 
                        task_type = self.task_type,
                        output_dimensionality = 3072 )
        )
        if not result.embeddings:
            raise ValueError( "GenAI embedding returned no embeddings." )
        
        return [ embedding.values for embedding in result.embeddings if embedding.values is not None ]
    
    @staticmethod
    def name() -> str:
        return "GenAIEmbeddingFunction"
    
    def get_config(self) -> dict[ str, Any ]:
        pass

    @staticmethod
    def build_from_config(config: dict[ str, Any ]) -> "EmbeddingFunction[D]":
        pass