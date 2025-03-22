import os
from google import genai
from google.genai import types

class GenerativeAIService():

    API_KEY = os.getenv( "GEMINI_API_KEY" )

    client = genai.Client( api_key = API_KEY )
    model = "gemini-2.0-flash"
    content_config = types.GenerateContentConfig( 
                        system_instruction = "堅持在醫療保健的領域內 提供使用者專業又溫暖的建議\n並請盡量以簡單明瞭且長話短說的方式回答以下使用者的問題:" )
    
    def answer( cls, question ):  
        response = cls.client.models.generate_content(
                                            model = cls.model,
                                            config = cls.content_config,
                                            contents = [ question ] )
        return response.text
    
    async def stream_answer( cls, question ):  
        response = cls.client.models.generate_content_stream( 
                                                model = cls.model,
                                                config = cls.content_config,
                                                contents = [ question ] )
        for chunk in response:
            yield chunk.text

    @classmethod
    def create_chat( cls ):
        chat = cls.client.chats.create( model = cls.model,
                                        config = cls.content_config )

        return chat