import time
from fastapi import HTTPException, Request, status
from app.auth.jwt import decode_access_token
from app.schemas.heart import HeartDiseaseRecord
from app.schemas.liver import LiverDiseaseRecord
from app.schemas.user import UserProfile
from app.services.nosql import RecordService
from app.services.disease import DiseasePredictionService
from app.services.user import UserProfileService

def heart_record_service( request: Request ) -> RecordService:

    if not hasattr( request.app.state, "heart_record_service" ):
        request.app.state.heart_record_service = RecordService( HeartDiseaseRecord )

    return request.app.state.heart_record_service


def liver_record_service( request: Request ) -> RecordService:

    if not hasattr( request.app.state, "liver_record_service" ):
        request.app.state.liver_record_service = RecordService( LiverDiseaseRecord )

    return request.app.state.liver_record_service


def user_profile_service( request: Request ) -> UserProfileService:

    if not hasattr( request.app.state, "user_profile_service" ):
        request.app.state.user_profile_service = UserProfileService( UserProfile )
        
    return request.app.state.user_profile_service


def predict_service( request: Request ) -> DiseasePredictionService:

    return request.app.state.predict_service


def verify_jwt_token( request: Request ):
    
    try:
        auth_header = request.headers.get( "Authorization" )
        if not auth_header or not auth_header.startswith( "Bearer "):
            raise ValueError( "Invalid Authorization header format" )
           
        token = auth_header.split( " " )[ 1 ]
        claims = decode_access_token( token )
        claims.validate_exp( time.time(), 0 )

        return claims
    
    except Exception as e:
        print( e )
        raise HTTPException( status_code = status.HTTP_401_UNAUTHORIZED,
                            headers = { "WWW-Authenticate": "Bearer" },
                            detail = "Missing or invalid token" )