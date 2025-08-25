from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.auth.dependencies.token_utils import verify_jwt


router = APIRouter()

@router.post( "/token" )
async def vraify_token( request: Request ):

    claims = verify_jwt( request )
    print( "claims: ", claims )

    try:
        user_name = claims.get( "name", "user" )
        user_email = claims.get( "email" )

        return JSONResponse( content = { "name": user_name,
                                         "email": user_email, }, 
                             status_code = status.HTTP_200_OK )
    except Exception as e:
        print( e )
         
    return JSONResponse( content = { "message": "An error occurred" }, 
                         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR )


@router.post( "/me" )
async def get_me():
    pass

    