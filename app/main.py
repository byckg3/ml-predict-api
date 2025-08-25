import secrets
import gradio as gr
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.auth.dependencies.token_utils import auth_for_gradio
from app.auth.router import auth_router
from app.api.router import api_router
from app.api.chat import router
from app.core.config import web_settings
from app.core.db import MongoDB
from app.services.disease import DiseasePredictionService
from app.web.chatbot import chat_window
from app.web.bmi import bmi_calculator
from app.web.index import signin, main

@asynccontextmanager
async def app_lifespan( app: FastAPI ):

    monogo = MongoDB()
    await monogo.init_beanie()

    app.state.mongo = monogo
    app.state.db = monogo.db

    predict_service = DiseasePredictionService()
    await predict_service.models_init()

    app.state.predict_service = predict_service
    
    yield

    await monogo.close()
    chat_window.close()

app = FastAPI( lifespan = app_lifespan )
app.include_router( api_router )
app.include_router( auth_router )

app = gr.mount_gradio_app( app, 
                           bmi_calculator,
                           path = "/bmi",
                           auth_dependency = auth_for_gradio,
)

app = gr.mount_gradio_app( app, 
                           chat_window, 
                           path = "/chatbot",
                           auth_dependency = auth_for_gradio,
)

app = gr.mount_gradio_app( app, 
                           main, 
                           path = "/index",
                           auth_dependency = auth_for_gradio,
)

app = gr.mount_gradio_app( app, 
                           signin, 
                           path = "/signin",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [ "https://weiwei032835.github.io", 
                       web_settings().FRONTEND_URL ],
    allow_credentials = True,
    allow_methods = [ "*" ],
    allow_headers = [ "*" ]
)
app.add_middleware( SessionMiddleware, secret_key = secrets.token_urlsafe( 32 ) )

@app.get( "/" )
def greet_json():
    return { "Hello": "World" }

@app.get( "/check" )
async def check_status():
    if await app.state.mongo.ping_server():
        return { "status": "running" }
    else:
        return { "status": "error" }
    

# uvicorn app.main:app --reload
# python -m app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run( "app.main:app", host = "localhost", port = 8000, reload = True )