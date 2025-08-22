import gradio as gr
from app.web.chat import chat_manager

healthcare_helper = chat_manager.genai_service
def chat_function( question, history, request: gr.Request ):

    try:
        qas = []
        for past_content in history:
            qas.append( f"{past_content[ 'role' ]}: {past_content[ 'content' ]}" )

        rag_prompt = healthcare_helper.rag_prompt( question )
        # print( rag_prompt )
        qas.append( rag_prompt )

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