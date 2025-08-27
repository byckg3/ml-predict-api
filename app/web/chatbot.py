import httpx
import gradio as gr
from app.core.config import web_settings

def chat_function( question, history: list, request: gr.Request ):
    
    try:  
        url = web_settings().BACKEND_URL + "/api/chat/ask"
        access_token = request.cookies.get( "access_token" )
        csrf_token = request.cookies.get( "csrf_token" )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-CSRF-Token": csrf_token
        }

        payload = {
            "question": question,
            "history": history
        }

        with httpx.Client( headers = headers ) as client:
            with client.stream( "POST", url, json = payload ) as response:
                msg = ""
                for text in response.iter_text():
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