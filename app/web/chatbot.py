import httpx
import gradio as gr
from app.core.config import web_settings

def chat_function( question, history: list, request: gr.Request ):
    print( "Chat function called..." )
    try:  
        url = web_settings().BACKEND_URL + "/api/chat/ask"
        access_token = request.cookies.get( "access_token" )
        csrf_token = request.cookies.get( "csrf_token" )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-CSRF-Token": csrf_token
        }

        csrf_cookie = { "csrf_token": csrf_token }

        payload = {
            "user_input": question,
            "history": history
        }

        timeout = httpx.Timeout(
            connect = 15.0,
            read = 40.0,
            write = 10.0,
            pool = 5.0
        )
        with httpx.Client( headers = headers, 
                           cookies = csrf_cookie, 
                           timeout = timeout ) as client:
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
function_call_example1 = """
這是我的生理數據，可以幫我評估心臟病的風險嗎?
```json
{
    "age": 52,
    "sex": 1,
    "cp": 0,
    "trestbps": 125,
    "chol": 212,
    "fbs": 0,
    "restecg": 1,
    "thalach": 168,
    "exang": 0,
    "oldpeak": 1,
    "slope": 2,
    "ca": 2,
    "thal": 2,
    "target": 0
}
```
"""
function_call_example2 = """
這是我的身體狀況 可以幫我評估心臟病的風險嗎?
40歲男性 
空腹血糖122 mg/dl
"""

chat_window = gr.ChatInterface( fn = chat_function,
                                examples = [ "提供哪些服務?", 
                                             "該如何預防心臟病?", 
                                             "該如何預防肝病?", 
                                             function_call_example1, 
                                             function_call_example2 ],
                                # editable = True,
                                autofocus = True,
)