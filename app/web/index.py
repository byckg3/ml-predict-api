import gradio as gr

def greet( name ):
    return "Hello " + name + "!"


with gr.Blocks() as signin:

    signin_btn = gr.Button( "Sign in with Google" )
    signin_btn.click( fn = greet )