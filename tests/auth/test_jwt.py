import pytest
from authlib.jose.errors import ExpiredTokenError
from datetime import datetime, timedelta
from app.auth.dependencies.jwt_utils import create_access_token, decode_access_token

# @pytest.mark.current
def test_encoding_and_decoding_jwt_token():
    
    payload = { "sub": "tester" }

    token = create_access_token( payload, expires_delta = timedelta( milliseconds = 1 ) )
    claims = decode_access_token( token )
    # print( claims )

    assert isinstance( token, str )
    assert claims[ "sub" ] ==  payload[ "sub"]
    with pytest.raises( ExpiredTokenError ):
        claims.validate( datetime.now().timestamp() ) 