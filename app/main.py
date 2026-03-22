import gradio as gr
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api.auth.dependencies.jwt_utils import auth_for_gradio
from app.api.auth.router import auth_router
from app.api.router import api_router
from app.core.config import web_settings
from app.db.document.database import MongoDB
from app.db.relational.database import get_engine, get_session_factory, init_tables
from app.services.disease import DiseasePredictionService
from app.web.chatbot import chat_window, chat_window_css
from app.web.bmi import bmi_calculator, container_css
from app.web.index import signin, main, blocks_css

@asynccontextmanager
async def app_lifespan( app: FastAPI ):
    
    print( f"\nStarting up the application..." )
    
    monogo = MongoDB()
    await monogo.init()

    app.state.mongo = monogo
    app.state.mongo_db = monogo.db
    
    app.state.postgres_engine = get_engine()
    await init_tables( app.state.postgres_engine )
    app.state.postgres_session_factory = get_session_factory( app.state.postgres_engine )

    predict_service = DiseasePredictionService()
    await predict_service.models_init()

    app.state.predict_service = predict_service
    
    yield

    print( f"\nShutting down the application..." )
    
    await monogo.close()
    chat_window.close()
    

app = FastAPI( lifespan = app_lifespan )
app.include_router( api_router )
app.include_router( auth_router )

app = gr.mount_gradio_app( app, 
                           bmi_calculator,
                           path = "/bmi",
                           auth_dependency = auth_for_gradio,
                           css = container_css,
)

app = gr.mount_gradio_app( app, 
                           chat_window, 
                           path = "/chatbot",
                           auth_dependency = auth_for_gradio,
                           css = chat_window_css
)

app = gr.mount_gradio_app( app, 
                           main, 
                           path = "/index",
                           auth_dependency = auth_for_gradio,
                           css = blocks_css,
)

app = gr.mount_gradio_app( app, 
                           signin, 
                           path = "/signin",
                           css = blocks_css,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [ "https://weiwei032835.github.io", 
                       web_settings().FRONTEND_URL ],
    allow_credentials = True,
    allow_methods = [ "*" ],
    allow_headers = [ "*" ]
)
app.add_middleware( SessionMiddleware, secret_key = web_settings().SESSION_SECRET )

@app.get( "/" )
def greet_json():
    return { "Hello": "World" }

@app.get( "/check" )
async def check_status():
    if await app.state.mongo.ping_server():
        return { "status": "running" }
    else:
        return { "status": "error" }
    

# uvicorn app.main:app --host 127.0.0.1 --port 7860 --reload
# python -m app.main
# http://127.0.0.1:7860
if __name__ == "__main__":
    import uvicorn
    uvicorn.run( "app.main:app", host = "127.0.0.1", port = 7860, reload = True )