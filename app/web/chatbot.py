import gradio as gr
from app.web.chat import chat_manager

healthcare_helper = chat_manager.genai_service

# https://ai.google.dev/api/caching?hl=zh-tw#Content
def add_past_message( messages ):

    past = []
    for msg in messages:
        
        payload = { "role": "", "parts": [] }
        if msg[ "role" ] == "user":
            payload[ "role" ] = "user"

        else:
            payload[ "role" ] = "model"

        payload[ "parts" ].append( { "text": msg[ "content" ] } )
        past.append( payload )
        
    return past


def chat_function( question, history: list, request: gr.Request ):
    
    try:
        qas = add_past_message( history )
        
        rag_prompt = healthcare_helper.rag_prompt( question )
        qas.append( { "role": "user", "parts": [ { "text": rag_prompt } ] } )
        # print( qas )
        msg = ""
        for text in healthcare_helper.stream_answer( qas ):
            msg = msg + str( text )
            yield msg

    except Exception as e:
        print( e )
        yield "Oops! Something went wrong. Please try again later."
    
chat_window_css = """
.gradio-container {
    margin-left: auto;
    margin-right: auto;
    width: 1000px;
}
"""

chat_window = gr.ChatInterface( fn = chat_function,
                                examples = [ "提供哪些服務?", "該如何預防心臟病?", "該如何預防肝病?" ],
                                # editable = True,
                                type = "messages", 
                                autofocus = True,
                                css = chat_window_css,
)