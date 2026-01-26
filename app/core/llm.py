from dataclasses import dataclass
from typing import AsyncIterator, Literal
from google import genai
from google.genai import errors
from google.genai import types

from app.core.config import gemini_settings

@dataclass
class LLMEvent:
    type: Literal[ "text", "tool_call", "done", "error" ]
    
    # streaming text
    content: str | None = None

    # tool call
    tool_name: str | None = None
    tool_args: dict | None = None
    
    # done only
    turn_contents: list[ types.Part ] | None = None

    error_code: int | str | None = None
    error_message: str | None = None
    retriable: bool = False
    
class GeminiClient:
    
    API_KEY = gemini_settings().API_KEY
    DEFAULT_MODEL = gemini_settings().MODEL_NAME
    candidate_model_names = [ "gemini-3-flash-preview","gemini-2.5-flash" ]
    
    def __init__( self, config ):
        self.content_config = config
        self.client = genai.Client( api_key = self.API_KEY )
        print( f"Initialized Gemini API client with model {self.DEFAULT_MODEL}" )
    
    def generate_text( self, question ):
        response = self.client.models.generate_content(
                        model = self.DEFAULT_MODEL,
                        contents = [ question ] )
        
        return response.text
    
    async def generate_text_stream( self, qa_records )-> AsyncIterator[LLMEvent]:
        
        try:
            response_stream  = await self.client.aio.models.generate_content_stream( 
                                model = self.DEFAULT_MODEL,
                                config = self.content_config,
                                contents = qa_records )
            
            accumulated_parts = []
            async for chunk in response_stream :

                if not chunk.candidates or \
                   not chunk.candidates[ 0 ].content or \
                   not chunk.candidates[ 0 ].content.parts:
                    continue

                parts = chunk.candidates[ 0 ].content.parts
                
                for part in parts:
                    accumulated_parts.append( part )
                    
                    if part.function_call:
                        # all_function_calls.append( part.function_call )
                        yield LLMEvent(
                            type = "tool_call",
                            tool_name = part.function_call.name,
                            tool_args = part.function_call.args,
                        )
                    
                    if part.text:
                        yield LLMEvent(
                            type = "text",
                            content = part.text,
                        )
                        
            yield LLMEvent( type = "done", turn_contents = accumulated_parts )

        except errors.ServerError as e:
            print( e )
            print( f"server error message:\n{e.message}" )
            
            yield LLMEvent(
                type = "error",
                error_code = f"{e.code} {e.status}",
                error_message = f"\n{e.message}",
            )
            
        except errors.ClientError as e:
            print( e )
            print( f"client error message:\n{e.message}" )
            
            yield LLMEvent(
                type = "error",
                error_code = f"{e.code} {e.status}",
                error_message = f"\n{e.message}",
            )
            
        except Exception as e:
            print( e )
            yield LLMEvent(
                type = "error",
                error_code = "UNKNOWN_ERROR",
                error_message = f"發生未知錯誤：{e}",
            )
            
    def create_chat( self ):
        chat = self.client.chats.create( 
                        model = self.DEFAULT_MODEL,
                        config = self.content_config )
        
        return chat