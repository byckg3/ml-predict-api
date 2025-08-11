import secrets
import gradio as gr
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.auth.google_auth import auth_router
from app.api.router import api_router
from app.core.db import MongoDB
from app.services.disease import DiseasePredictionService
from app.web.chat import chat_router
from app.web.widget import web_router, chat_window

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
app.include_router( auth_router, tags = [ "Auth" ] )
app.include_router( chat_router )
app.include_router( web_router )

app = gr.mount_gradio_app( app, chat_window, path = f"{web_router.prefix}/chat" )

app.add_middleware(
    CORSMiddleware,
    allow_origins =  [ "https://weiwei032835.github.io" ],
    allow_credentials = True,
    allow_methods = [ "*" ],
    allow_headers = [ "*" ]
)
app.add_middleware( SessionMiddleware, secret_key = secrets.token_urlsafe( 32 ) )

@app.get( "/hello" )
def greet_json():
    return { "Hello": "World!" }

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