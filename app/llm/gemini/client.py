from dataclasses import dataclass
from typing import Any, AsyncIterator, Literal
from google import genai
from google.genai import types, errors

from app.core.config import gemini_settings
from app.llm.domain.models import LLMResponse, ToolCall
    
class GeminiClient:
    
    API_KEY = gemini_settings().API_KEY
    DEFAULT_MODEL = gemini_settings().MODEL_NAME
    candidate_model_names = [ "gemini-3-flash-preview", "gemini-2.5-flash" ]
    
    def __init__( self, config ):
        self.content_config = config
        self.client = genai.Client( api_key = self.API_KEY )
        print( f"Initialized Gemini API client with model {self.DEFAULT_MODEL}" )
        
        self.request_adapter = RequestAdapter()
    
    
    def generate_text( self, question ):
        response = self.client.models.generate_content(
                        model = self.DEFAULT_MODEL,
                        contents = [ question ] )
        
        return response.text
    
    
    async def generate_text_stream( self, prompts )-> AsyncIterator[ LLMResponse ]:
        
        try:
            response_stream  = await self.client.aio.models.generate_content_stream( 
                                    model = self.DEFAULT_MODEL,
                                    config = self.content_config,
                                    contents = prompts )
            
            response_adapter = ResponseAdapter()
            parsed_response_stream = response_adapter.parse_response_stream( response_stream )
            async for llm_response in parsed_response_stream:
                yield llm_response
            
            full_response = response_adapter.parse_parts( response_adapter.accumulated_parts )
            full_response.is_final = True
            
            yield full_response

        except errors.ServerError as e:
            print( e )
            print( f"server error message:\n{e.message}" )
            
            yield LLMResponse(
                error_code = f"{e.code} {e.status}",
                error_message = f"\n{e.message}",
            )
            
        except errors.ClientError as e:
            print( e )
            print( f"client error message:\n{e.message}" )
            
            yield LLMResponse(
                error_code = f"{e.code} {e.status}",
                error_message = f"\n{e.message}",
            )
            
        except Exception as e:
            print( e )
            yield LLMResponse(
                error_code = "UNKNOWN_ERROR",
                error_message = f"發生未知錯誤：{e}",
            )
            
    def create_chat( self ):
        chat = self.client.chats.create( 
                    model = self.DEFAULT_MODEL,
                    config = self.content_config )
        
        return chat


class RequestAdapter:
    
    def __init__( self ):
        pass

    # https://ai.google.dev/api/caching?hl=zh-tw#Content
    def build_chat_request( self, prompt: str, history: list = [] ):
        
        contents = []
        for content in history:
            
            payload = { "role": "user", "parts": [] }
            if content[ "role" ] != "user":
                payload[ "role" ] = "model"

            payload[ "parts" ].append( types.Part.from_text( text = content.get( "content", "" ) ) )
            contents.append( payload )
        
        text_content = self.build_text_content( prompt )
        contents.append( text_content )
            
        return contents
    
    def build_text_content( self, text: str, role: str = "user" ):
        return types.Content(
            role = role, 
            parts = [ types.Part.from_text( text = text ) ]
        )
        
    def build_content( self, items: list[ Any ], role: str = "user" ) -> types.Content:
        return types.Content( role = role, parts = items )
    
    # https://ai.google.dev/api/caching#FunctionResponse
    def build_content_from_tool_call( self, tool_contents: list[ ToolCall ] ):
        
        tool_parts = []
        for tool_content in tool_contents:
        
            if tool_content.output:
                
                function_response: dict[ str, Any ] = { "result": tool_content.output }
                tool_parts.append(
                    types.Part.from_function_response(
                        name = tool_content.name,
                        response = function_response,
                    )
                )
        
        return types.Content(
            role = "user", 
            parts = tool_parts
        )


class ResponseAdapter:
    
    def __init__( self ):
        self.accumulated_parts: list[ types.Part ] = []
        
    
    def parse_response( self, response: types.GenerateContentResponse ) :
        # to do
        pass
    
    async def parse_response_stream( self, stream: AsyncIterator[ types.GenerateContentResponse ] ):
        
        async for chunk in stream :
            
            if not chunk.candidates or \
               not chunk.candidates[ 0 ].content or \
               not chunk.candidates[ 0 ].content.parts:
                continue
            
            parts: list[ types.Part ] = chunk.candidates[ 0 ].content.parts
            for part in parts:
                
                self.accumulated_parts.append( part )
                if part.function_call:
                    
                    yield LLMResponse(
                        tool_name = part.function_call.name,
                        tool_args = part.function_call.args,
                    )
                
                if part.text:
                    yield LLMResponse( text = part.text )
                
    
    def parse_parts( self, parts: list[ types.Part ] ) -> LLMResponse:
        
        current_text = ""
        parsed_parts = []
        for part in parts:
            
            if part.text:
                current_text += part.text
                
            else:
                if current_text:
                    parsed_parts.append( types.Part( text = current_text ) )
                    current_text = ""
                
            parsed_parts.append( part )
            
        return LLMResponse( contents = parsed_parts )