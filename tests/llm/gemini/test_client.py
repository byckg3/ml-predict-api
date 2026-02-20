import pytest
from google.genai import types
from app.llm.dto import LLMResponse
from app.llm.gemini.client import GeminiClient, RequestAdapter

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

    async def test_generate_text_stream( self, gemini_client: GeminiClient ):
        
        reponse_stream = gemini_client.generate_text_stream( "請給一個1~100的幸運數字" )
        
        all_function_calls: list[ LLMResponse ] = []
        async for response in reponse_stream:
            
            if response.text:
                text_chunk = response.text
                
                print( text_chunk, end = "", flush = True )
                
            if response.tool_name:
                all_function_calls.append( response )
                
        # print( all_function_calls[ 0 ].tool_args)
        assert len( all_function_calls ) == 1
        assert all_function_calls[ 0 ].tool_name == "predict_lucky_number"
        assert all_function_calls[ 0 ].tool_args is not None

# @pytest.mark.test_only
class TestRequestAdapter:
    
    @pytest.fixture
    def request_adapter( self ) -> RequestAdapter:
        return RequestAdapter()
    
    def test_build_content_with_text_parts_and_custom_role( self, request_adapter: RequestAdapter ):
        
        items = [ types.Part.from_text( text = "Hello" ), 
                  types.Part.from_text( text = "World" ) 
        ]
        content: types.Content = request_adapter.build_content( items, role = "model" )
        
        expected_content = {
            "role": "model",
            "parts": [
                { "text": "Hello" },
                { "text": "World" }
            ]
        }
        
        assert content.model_dump( exclude_none = True ) == expected_content