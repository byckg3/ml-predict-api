from uuid import UUID
from datetime import datetime
from typing import Annotated
from beanie import Document, Indexed
from pydantic import ConfigDict, EmailStr, Field
from pydantic.config import JsonDict

from app.core.schemas import BaseSchema, TimestampSchema

examples: dict[ str, JsonDict ] = {
    "login_info": {
        "email": f"mike123456@email.com"
    },
    "base_profile": {
        "name": "Mike",
        "email": f"mike{ int( datetime.now().timestamp() ) }@email.com"
    },
    "created_profile": {
        "public_id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Mike",
        "email": f"mike{ int( datetime.now().timestamp() ) }@email.com"
    }
}


class UserBase( TimestampSchema, BaseSchema ):
    
    name: str | None = Field( max_length = 20, default = None )
    email: EmailStr = Field( max_length = 30 )

class UserProfile( UserBase ):
    
    public_id: UUID

    model_config = ConfigDict(
        json_schema_extra = {
            "examples": [ 
                examples[ "created_profile" ]
            ]
        }
        
    )
    
class UserPatch( BaseSchema ):
    
    name: str | None = Field( max_length = 20, default = None )
    email: EmailStr | None = Field( max_length = 30, default = None )
    
    model_config = ConfigDict(
        json_schema_extra = {
            "examples": [ 
                examples[ "base_profile" ]
            ]
        }
        
    )