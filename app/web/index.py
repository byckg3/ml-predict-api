import gradio as gr

def greet( request: gr.Request ):
    # if request:
    #     print( "Request headers dictionary:", request.headers )
    #     print( "IP address:", request.client.host )
    #     print( "Query parameters:", dict( request.query_params ) )
    #     print( f"Hello {request.username}!\n" )

    return f"## Welcome, {request.username}"

blocks_css = """
.center {
    margin-left: auto;
    margin-right: auto;
    width: 300px;
}
.center-text { text-align: center; }
"""

with gr.Blocks( css = blocks_css ) as signin:

    signin_btn = gr.Button( "Sign in with Google", 
                            link = "/auth/google/login", 
                            elem_classes = "center",
    )


with gr.Blocks( css = blocks_css ) as main:
    with gr.Column( variant = "compact" ):
        m = gr.Markdown( "## Welcome to Gradio!",
                         elem_classes = [ "center", "center-text" ], )
        gr.Button( "Logout", 
                   link = "/logout",
                   elem_classes = "center", )

    main.load( greet, None, m )