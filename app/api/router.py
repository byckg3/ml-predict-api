from fastapi import APIRouter, Depends
from app.api.v1.router import v1_router
from app.api.v2.router import v2_router
from app.api.auth.dependencies.csrf_utils import verify_csrf_token
from app.api.auth.dependencies.jwt_utils import verify_jwt

api_router = APIRouter( prefix = "/api", 
                        # dependencies = [ Depends( verify_csrf_token ), 
                        #                  Depends( verify_jwt ),  ] 
)
api_router.include_router( v1_router )
api_router.include_router( v2_router )