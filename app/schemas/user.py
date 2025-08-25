from datetime import datetime
from typing import Annotated
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from app.schemas.base import BaseEntity

example = {
    "login_info": {
        "email": f"mike123456@email.com"
    },
    "created_profile": {
        "name": "Mike",
        "email": f"mike{ int( datetime.now().timestamp() ) }@email.com"
    }
}

class UserProfile( BaseEntity, Document ):
    
    name: str | None = "unknown"
    email: Annotated[ EmailStr, Indexed( unique = True ) ] = Field( max_length = 30,
                                                                    examples = [ "mike123456@email.com" ] )
    class Settings:
        name = "users"

    model_config = {
        "json_schema_extra": {
            "examples": [ example[ "created_profile" ] ]
        }
    }