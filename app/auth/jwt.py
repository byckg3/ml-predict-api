from datetime import datetime, timezone
from authlib.jose import jwt

SECRET_KEY = "your-own-secret-key"
header = { "alg": "HS256" }

def create_access_token( payload: dict, expires_delta ):

    payload.update( { "exp": datetime.now( timezone.utc ) + expires_delta } )
    token_bytes: bytes = jwt.encode( header, payload, SECRET_KEY )
    
    return token_bytes.decode( "utf-8" )


def decode_access_token( token: str ):

    claims = jwt.decode( token, SECRET_KEY )

    return claims