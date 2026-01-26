import pytest
from google import genai
from google.genai import types
from app.core.llm import GeminiClient

def predict_lucky_number( min_int, max_int ) -> int:
    return 1

predict_function = {
    "name": "predict_lucky_number",
    "description": "當使用者要求在某個數字範圍內預測出幸運號碼時，請呼叫此函式",
    "parameters": {
        "type": "object",
        "properties": {
            "min_int": {
                "type": types.Type.INTEGER,
                "description": "使用者提供的幸運號碼範圍內的最小值",
            },
            "max_int": {
                "type": types.Type.INTEGER,
                "description": "使用者提供的幸運號碼範圍內的最大值",
            },
        },
        "required": [ "min_int", "max_int" ],
    },
}

@pytest.mark.current
class TestGeminiClient:
    
    @pytest.fixture
    def gemini_client( self ):
        
        tools = types.Tool( 
            function_declarations = [ 
                types.FunctionDeclaration( **predict_function ) 
            ] 
        )
        test_config = types.GenerateContentConfig( 
            tools = [ tools ],
            system_instruction = "盡量以簡單明瞭的方式回答使用者的問題，如果被要求給出一個幸運數字，請呼叫 predict_lucky_number 函式來預測幸運號碼。"
        )
        client = GeminiClient( config = test_config )

        yield client

        del client

    async def test_generate_text_stream( self, gemini_client ):
        
        event_stream = gemini_client.generate_text_stream( "請給一個1~100的幸運數字" )
        
        all_function_calls = []
        async for event in event_stream:
            
            if event.type == "text":
                text_chunk = event.content or ""
                
                print( text_chunk, end = "", flush = True )
                
            if event.type == "tool_call":
                
                all_function_calls.append( event )
                
                min_int = event.tool_args.get( "min_int", 1 )
                max_int = event.tool_args.get( "max_int", 100 )
                
                lucky_number = predict_lucky_number( min_int, max_int )
                
                print( f"\n預測的幸運號碼是: {lucky_number}\n" )
                
        assert len( all_function_calls ) == 1
        assert all_function_calls[ 0 ].tool_name == "predict_lucky_number"
        assert all_function_calls[ 0 ].tool_args is not None
        print( all_function_calls[ 0 ].tool_args)