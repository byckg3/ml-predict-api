from google import genai
from google.genai import errors
from google.genai import types

from app.core.config import gemini_settings

class GeminiAPIClient:
    
    API_KEY = gemini_settings().API_KEY
    DEFAULT_MODEL = gemini_settings().MODEL_NAME
    
    def __init__( self, system_prompt: str | None = None ):
        self.content_config = types.GenerateContentConfig( 
                                    system_instruction = system_prompt )
        
        self.client = genai.Client( api_key = self.API_KEY )
        print( f"Initialized Gemini API client with model {self.DEFAULT_MODEL}" )
    
    def generate_text( self, question ):
        response = self.client.models.generate_content(
                        model = self.DEFAULT_MODEL,
                        contents = [ question ] )
        
        return response.text
    
    async def generate_text_stream( self, qa_records ):
        
        try:
            response = await self.client.aio.models.generate_content_stream( 
                                model = self.DEFAULT_MODEL,
                                config = self.content_config,
                                contents = qa_records )
                                            
            async for chunk in response:
                yield chunk.text
                
        except errors.ServerError as e:
            print( e )
            print( f"server error message:\n{e.message}" )
            
            yield e.message
            
        except errors.ClientError as e:
            print( e )
            print( f"client error message:\n{e.message}" )
            
            yield e.message
            
        except Exception as e:
            yield f"發生未知錯誤：{e}"
            
    def create_chat( self ):
        chat = self.client.chats.create( 
                        model = self.DEFAULT_MODEL,
                        config = self.content_config )
        
        return chat