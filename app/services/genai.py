from typing import Any
from chromadb import Documents, EmbeddingFunction, Embeddings
from fastapi import WebSocket
from google import genai
from google.genai import types

from app.core.config import gemini_settings
from app.core.llm import GeminiClient, LLMEvent
from app.repositories.embed import ChromaRepository
from app.schemas.heart import HeartDiseaseFeatures
from app.schemas.prompt import HealthCare
from app.services.disease import DiseasePredictionService

class GeminiService:
    
    def __init__( self, predict_service: DiseasePredictionService, domain = HealthCare ):
        self.domain = domain
        tools = types.Tool( 
            function_declarations = [ 
                types.FunctionDeclaration( **self.domain.function_declarations[ "predict_heart_risk" ] ) 
            ] 
        )
        config = types.GenerateContentConfig( 
            tools = [ tools ],
            system_instruction = self.domain.system_prompt
        )
        self.risk_prediction_service = predict_service
        self.embed_repository = ChromaRepository( function = GenAIEmbeddingFunction() )
        self.client = GeminiClient( config )
    
    def answer( self, question ):
        response = self.client.generate_text( question )
        return response
    
    
    async def streaming_answer( self, qa_records ):
        contents: list = qa_records
        
        while True:
            print( f"Sending contents to LLM: {contents}" )
            event_stream = self.client.generate_text_stream( contents )
            
            all_function_calls: list[ LLMEvent ] = []
            async for event in event_stream:
                
                if event.type == "text":
                    text_chunk = event.content or ""
                    
                    yield text_chunk
                
                elif event.type == "tool_call":
                    all_function_calls.append( event )
                    
                elif event.type == "done":
                    contents.append( types.Content( role = "model", parts = event.turn_contents ) )
                    
                else:
                    yield f"\nError: {event.error_code}\n{event.error_message}\n"
            
            if not all_function_calls:
                break
            
            function_response_parts = []
            for fc in all_function_calls:
                
                print( f"Function to call: {fc.tool_name}" )
                print( f"Arguments: {fc.tool_args}" )
                yield f"\n[評估中...]\n"
                
                result = "error"
                if fc.tool_name == "predict_heart_risk":
                    result = self.risk_prediction_service.predict_heart_risk( HeartDiseaseFeatures( **fc.tool_args ) ) # type: ignore
                    print( f"result: {result}" )   

                    function_response_parts.append(
                        types.Part.from_function_response(
                            name = fc.tool_name,
                            response = { "result": result },
                        ) 
                    )

            contents.append( types.Content( role = "user", parts = function_response_parts ) )

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
        self.genai_service = GeminiService( DiseasePredictionService())

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
    
    def get_config(self) -> dict[ str, Any ]: # type: ignore
        pass

    @staticmethod
    def build_from_config(config: dict[ str, Any ]) -> "EmbeddingFunction[D]": # type: ignore
        pass