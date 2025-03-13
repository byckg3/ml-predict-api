from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router import api_router
from app.models.db import MongoDB

@asynccontextmanager
async def app_lifespan( app: FastAPI ):

    monogo = MongoDB()
    await monogo.init_beanie()

    app.state.mongo = monogo
    app.state.db = monogo.db
    
    yield

    await monogo.close()

app = FastAPI( lifespan = app_lifespan )
app.include_router( api_router )

@app.get( "/check" )
async def check_status():
    if await app.state.mongo.ping_server():
        return {"status": "running" }
    else:
        return {"status": "error" }
    

# uvicorn app.main:app --reload
# python -m app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run( "app.main:app", host = "localhost", port = 8000, reload = True )