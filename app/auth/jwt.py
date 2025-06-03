from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "your-own-secret-key"
ALGORITHM = "HS256"

def create_access_token( to_encode: dict, expires_delta ):

    to_encode.update( { "exp": datetime.now( timezone.utc ) + expires_delta } )
    # print( "to_encode:",  to_encode )

    return jwt.encode( to_encode, SECRET_KEY, algorithm = ALGORITHM )


def decode_access_token( token: str ):

    payload = jwt.decode( token, SECRET_KEY, algorithms = ALGORITHM )

    return payload