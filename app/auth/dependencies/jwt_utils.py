import time
from fastapi import HTTPException, Request, status
from datetime import datetime, timezone
from authlib.jose import jwt
from app.core.config import web_settings

SECRET_KEY = web_settings().JWT_SECRET
header = { "alg": "HS256" }

def create_access_token( payload: dict, expires_delta ):

    payload.update( { "exp": datetime.now( timezone.utc ) + expires_delta } )
    token_bytes: bytes = jwt.encode( header, payload, SECRET_KEY )
    
    return token_bytes.decode( "utf-8" )


def decode_access_token( token: str ):

    claims = jwt.decode( token, SECRET_KEY )

    return claims


def verify_jwt( request: Request ):
    
    jwt = get_jwt_from_header_or_cookie( request  )

    try:
        claims = decode_access_token( jwt )
        claims.validate_exp( time.time(), 0 )

        return claims
    
    except Exception as e:
        print( e )
        raise HTTPException( status_code = status.HTTP_401_UNAUTHORIZED,
                             headers = { "WWW-Authenticate": "Bearer" },
                             detail = "Not authenticated" )

def get_jwt_from_header_or_cookie( request: Request,  ) -> str:
   
    auth_header = request.headers.get( "Authorization" )
    if auth_header and auth_header.startswith( "Bearer " ):
        return auth_header.split( " ", 1 )[ 1 ]

    token = request.cookies.get( "access_token" )
    
    if token:
        return token

    raise HTTPException( status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token not found" )

def auth_for_gradio( request: Request ):

    claims: dict = verify_jwt( request )
    # print( claims ) # {'_id': '683d84e3d4edf69bd12d170b', 'name': 'John', 'email': 'example@gmail.com', 'exp': 1755979834}

    if claims:
        return claims.get( "name", "user" )
    
    else:
        return None