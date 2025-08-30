import secrets
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from app.api.user import ServiceDependency
from app.auth.dependencies.csrf_utils import create_csrf_token
from app.auth.dependencies.jwt_utils import create_access_token
from app.core.config import google_auth_settings, web_settings
from cachetools import TTLCache

oauth = OAuth()
oauth.register(
        name = "google",
        server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
        client_id = google_auth_settings().CLIENT_ID,
        client_secret = google_auth_settings().CLIENT_SECRET,
        client_kwargs = {
            "scope": "openid email profile"
        }
)
otc_store = TTLCache( maxsize = 1000, ttl = 300 )

router = APIRouter( prefix = "/google" )

@router.get( "/login" )
async def login_via_google( request: Request ):
    
    redirect_uri = request.url_for( "auth_via_google" )
    # print( "\nredirect_uri:", redirect_uri )
    
    return await oauth.google.authorize_redirect( request, redirect_uri ) # type: ignore


@router.get( "/callback" )
async def auth_via_google( request: Request, user_service: ServiceDependency ):

    try:
        token = await oauth.google.authorize_access_token( request ) # type: ignore
      
        user_info = token[ "userinfo" ]
        # print( "google_user_info:\n", user_info )
        user_profile = await user_service.find_or_create_by_email( user_info )
        user_json = jsonable_encoder( user_profile, exclude = { "created_at", "updated_at" } )

    except OAuthError as error:
        print( "OAuthError:", error )
        raise HTTPException( status_code = status.HTTP_401_UNAUTHORIZED, 
                             detail = "Google authentication failed." )
    
    except Exception as e:
        print( e )
        raise HTTPException( status_code = 500, detail = "An error occurred." )
    
    redirect_url = web_settings().FRONTEND_URL + "/index"
    response = RedirectResponse( redirect_url )
    set_jwt_cookie_for_frontend( user_json, response )
    set_csrf_cookie_for_frontend( response )

    # code, response = set_one_time_code_for_frontend( redirect_url )
    # otc_store[ code ] = user_json

    return response


@router.post( "/exchange" )
async def exchange_code( payload: dict ):

    try:
        code = payload[ "otc" ]

        if code and code in otc_store:
            user_data = otc_store.pop( code )
            jwt_token = create_access_token( user_data )

            return JSONResponse( content = { "access_token": jwt_token }, 
                                 status_code = status.HTTP_200_OK )

    except Exception as e:
        print( e )

    raise HTTPException( status_code = status.HTTP_400_BAD_REQUEST, 
                         detail = "Exchange otc failed." )


# @router.post( "/token" )
async def token( request: Request ):
    data = await request.json()
    print( "data:",data["id_token"] )  
    claims = await oauth.google.parse_id_token( token =  data, nonce = None) # type: ignore
    # print( claims ) 

def set_jwt_cookie_for_frontend( data_payload: dict, response: RedirectResponse ):

    jwt_token = create_access_token( data_payload )
    # print( f"jwt: {jwt_token}" )

    response.set_cookie( 
        key = "access_token",
        value = jwt_token, 
        httponly = True,
        secure = True,  
        samesite = "none",  # "strict", "lax", "none"
        max_age = 3600,
    )

def set_csrf_cookie_for_frontend( response: RedirectResponse ):

    csrf_token = create_csrf_token()
    print( "csrf:", csrf_token )
    response.set_cookie(
        key = "csrf_token",
        value = csrf_token,
        httponly = False,
        secure = True,
        samesite = "none",
        max_age = 3600,
    )

def set_one_time_code_for_frontend( redirect_url ):

    one_time_code = secrets.token_urlsafe( 16 )
    redirect_url = redirect_url + f"#otc={one_time_code}"

    return one_time_code, RedirectResponse( redirect_url )