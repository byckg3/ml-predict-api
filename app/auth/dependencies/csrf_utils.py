import secrets
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyCookie, APIKeyHeader

def create_csrf_token():

    return secrets.token_urlsafe( 32 )

header_scheme = APIKeyHeader( name = "X-CSRF-Token", auto_error = True )
cookie_scheme = APIKeyCookie( name = "csrf_token", auto_error = True )

def verify_csrf_token( csrf_header: str = Depends( header_scheme ),
                       csrf_cookie: str = Depends( cookie_scheme ) ):

    # csrf_cookie = request.cookies.get( "csrf_token" )
    # csrf_header = request.headers.get( "X-CSRF-Token" )

    if csrf_cookie != csrf_header:

        raise HTTPException( status_code = status.HTTP_403_FORBIDDEN,
                             detail = "CSRF token invalid" )