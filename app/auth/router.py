from fastapi import APIRouter
from app.auth import google, verifier

auth_router = APIRouter( prefix = "/auth" )
auth_router.include_router( google.router, tags = [ "Google Auth" ] )
auth_router.include_router( verifier.router, tags = [ "Verification" ] )