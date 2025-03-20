import os
from google import genai
from google.genai import types

class GenerativeAIService():

    API_KEY = os.getenv( "GEMINI_API_KEY" )

    def __init__( self ):
        self.client = genai.Client( api_key = GenerativeAIService.API_KEY )
        self.model = "gemini-2.0-flash"
        self.content_config = types.GenerateContentConfig( 
                                system_instruction = "堅持在醫療保健的領域內 提供使用者專業又溫暖的建議" )

    
    def answer( self, question ):  
        response = self.client.models.generate_content(
                                                model = self.model,
                                                config = self.content_config,
                                                contents = [ question ] )
        
        return response.text
    
    async def stream_answer( self, question ):  
        response = self.client.models.generate_content_stream( 
                                                model = self.model,
                                                config = self.content_config,
                                                contents = [ question ] )
        for chunk in response:
            yield chunk.text
