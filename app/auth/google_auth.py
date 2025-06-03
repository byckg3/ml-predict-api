from authlib.integrations.starlette_client import OAuth, OAuthError
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.user import ServiceDependency
from app.auth.jwt import create_access_token
from app.core.config import google_auth_settings, web_settings
from app.schemas.user import UserProfile

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

auth_router = APIRouter( prefix = "/auth" )

@auth_router.get( "/google/callback" )
async def auth_via_google( request: Request, user_service: ServiceDependency ):

    try:
        token = await oauth.google.authorize_access_token( request )
      
        user_info = token[ "userinfo" ]
        # print( "google_user_info:\n", user_info )
        user_profile = await user_service.find_or_create_by_email( user_info )

    except OAuthError as error:
        print( "OAuthError:", error )
        raise HTTPException( status_code = status.HTTP_401_UNAUTHORIZED, 
                             detail = "Google authentication failed." )
    
    except Exception as e:
        print( e )
        raise HTTPException( status_code = 500, detail = "An error occurred." )
    

    json_profile = jsonable_encoder( user_profile, exclude = { "created_at", "updated_at" } )
    expires_delta = timedelta( minutes = 15 )
    jwt_token = create_access_token( json_profile, expires_delta )
    print( f"jwt:\n{jwt_token}" )

    # return JSONResponse( content = { "access_token": jwt_token,
    #                                  "token_type": "bearer",
    #                                  "expires_in": int( expires_delta.total_seconds() ),
    #                                  #  "user_profile": json_profile 
    #                      }, 
    #                      status_code = status.HTTP_200_OK )

    redirect_url = web_settings().FRONTEND_URL + f"#{jwt_token}"
    response = RedirectResponse( redirect_url )
    # response.set_cookie( key = "access_token",
    #                      value = jwt_token,
    #                      httponly = True,
    #                      secure = True,  
    #                      samesite = "strict",  # Set the SameSite attribute to None
    # )
    return response

@auth_router.get( "/google/login" )
async def login_via_google( request: Request ):
    
    redirect_uri = request.url_for( "auth_via_google" )
    # print( "\nredirect_uri:", redirect_uri )
    
    return await oauth.google.authorize_redirect( request, redirect_uri )


@auth_router.post( "/google/token" )
async def token( request: Request ):
    data = await request.json()
    print( "data:",data["id_token"] )  
    claims = await oauth.google.parse_id_token( token =  data, nonce = None)
    # print( claims )        