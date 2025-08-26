import gradio as gr

def greet( request: gr.Request ):
    if request.username:
    #     print( "Request headers dictionary:", request.headers )
    #     print( "IP address:", request.client.host )
    #     print( "Query parameters:", dict( request.query_params ) )
    #     print( f"Hello {request.username}!\n" )
        return f"# Welcome, {request.username}"
    else:
        return "# Welcome, visitor"

text_template = """
- [chatbot](/chatbot)
- [bmi calculator](/bmi)
"""
def display_links():
    return text_template

blocks_css = """
.center {
    margin-left: auto;
    margin-right: auto;
    width: 300px;
}
.center-text { text-align: center; }
.gradio-container {
    margin-left: auto;
    margin-right: auto;
    width: 400px;
    height: 700px;
}
"""

with gr.Blocks( css = blocks_css ) as signin:
    gr.Markdown( "## Welcome to Gradio!", elem_classes = [ "center-text" ] )
    signin_btn = gr.Button( "Sign in with Google", 
                            link = "/auth/google/login", 
                            elem_classes = [ "center" ],
    )

with gr.Blocks( css = blocks_css ) as main:
    with gr.Column():
        title = gr.Markdown( elem_classes = [ "center-text" ], )
        links = gr.Markdown( "",  )
        gr.Button( "Logout", 
                   link = "/signin",
                   elem_classes = [ "center" ], )

    main.load( greet, None, title )
    main.load( display_links, None, links )