from fastapi import APIRouter, FastAPI
from app.api.router import api_router

app = FastAPI()
app.include_router( api_router )

@app.get( "/check" )
def check_status():
    return { "status": "running" }

# uvicorn app.main:app --reload
# python -m app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run( "app.main:app", host = "localhost", port = 8000, reload = True )