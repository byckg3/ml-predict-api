from typing import Any
from chromadb import Documents, EmbeddingFunction
from google import genai
from google.genai import types

from app.core.config import gemini_settings
from app.llm.domain.models import ToolCall
from app.llm.gemini.client import GeminiClient, RequestAdapter
from app.repositories.embed import ChromaRepository
from app.schemas.chat import ChatPayload
from app.schemas.heart import HeartDiseaseFeatures
from app.schemas.prompt import HealthCare
from app.services.disease import DiseasePredictionService

class ChatService:
    
    def __init__( self, prediction_service: DiseasePredictionService, domain = HealthCare ):
        self.domain = domain
        tool = types.Tool( 
            function_declarations = [ 
                types.FunctionDeclaration( **self.domain.function_declarations[ "predict_heart_risk" ] ) 
            ] 
        )
        config = types.GenerateContentConfig( 
            tools = [ tool ],
            system_instruction = self.domain.system_prompt
        )
        self.risk_prediction_service = prediction_service
        self.embed_repository = ChromaRepository( function = GeminiEmbeddingFunction() )
        self.client = GeminiClient( config )
        self.llm_request_adapter = RequestAdapter()
        
    
    def answer( self, question ):
        response = self.client.generate_text( question )
        return response
    
    
    async def streaming_answer( self, chat_payload: ChatPayload ):
        
        augmented_prompt = self._augment_input( chat_payload.user_input )
        contents = self.llm_request_adapter.build_chat_request( augmented_prompt, history = chat_payload.history )
        
        while True:
            # print( f"Sending contents to LLM: {contents}" )
            llm_response_stream = self.client.generate_text_stream( contents )
            
            all_tool_calls: list[ ToolCall ] = []
            async for llm_response in llm_response_stream:
                
                if llm_response.text:
                    yield llm_response.text
                    
                elif llm_response.tool_name:
                    tool_call_content = ToolCall( name = llm_response.tool_name, args = llm_response.tool_args )
                    all_tool_calls.append( tool_call_content )
                    
                elif llm_response.is_final:
                    model_content = self.llm_request_adapter.build_content( role = "model", items = llm_response.contents  or [] )
                    contents.append( model_content )
                    
                else:
                    yield f"\nError: {llm_response.error_code}\n{llm_response.error_message}\n"
            
            if not all_tool_calls:
                break
            
            for fc in all_tool_calls:
                
                print( f"Function to call: {fc.name}" )
                print( f"Arguments: {fc.args}" )
                yield f"\n[評估中...]\n"
                
                result = "error"
                if fc.name == "predict_heart_risk":
                    
                    result = self.risk_prediction_service.predict_heart_risk( HeartDiseaseFeatures( **fc.args ) ) # type: ignore
                    fc.output = result
                    print( f"result: {result}" )
                    
                elif fc.name == "predict_liver_risk":
                    # to do
                    pass
                
                else:
                    print( f"Unknown tool call: {fc.name}" )

            tool_call_response_content = self.llm_request_adapter.build_content_from_tool_call( all_tool_calls )
            contents.append( tool_call_response_content )
            

    def _augment_input( self, question ):
      
        retrieved_context = self._retrieve_relevant_context( question )
        prompt = self.domain.chat_template.format( **retrieved_context )

        return prompt
    
    def _retrieve_relevant_context( self, user_input: str ):
        
        qas = self.embed_repository.find_qa_texts( user_input )
        docs = self.embed_repository.find_pdf_documents( user_input )

        retrieved_context = {
            "retrieved_content": "\n".join( qas ),
            "retrieved_document": "\n".join( docs ),
            "user_query": user_input
        }
        return retrieved_context
    

    def open_chat_session( self, domain = HealthCare ):
        return self.client.create_chat()
    

class GeminiEmbeddingFunction( EmbeddingFunction[ Documents ] ):
    
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
            contents = input, # type: ignore
            config = types.EmbedContentConfig( 
                        task_type = self.task_type,
                        output_dimensionality = 3072 )
        )
        if not result.embeddings:
            raise ValueError( "GenAI embedding returned no embeddings." )
        
        return [ embedding.values for embedding in result.embeddings if embedding.values is not None ]
    
    @staticmethod
    def name() -> str:
        return "GeminiEmbeddingFunction"
    
    def get_config(self) -> dict[ str, Any ]: # type: ignore
        pass

    @staticmethod
    def build_from_config(config: dict[ str, Any ]) -> "EmbeddingFunction[D]": # type: ignore
        pass