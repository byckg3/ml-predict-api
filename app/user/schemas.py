from uuid import UUID
from datetime import datetime
from typing import Annotated
from beanie import Document, Indexed
from pydantic import ConfigDict, EmailStr, Field
from pydantic.config import JsonDict

from app.core.schemas import Base

example: dict[ str, JsonDict ] = {
    "login_info": {
        "email": f"mike123456@email.com"
    },
    "created_profile": {
        "public_id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Mike",
        "email": f"mike{ int( datetime.now().timestamp() ) }@email.com"
    }
}


class UserBase( Base ):
    
    name: str | None = "unknown"
    email: Annotated[ EmailStr, Indexed( unique = True ) ] = Field( max_length = 30,
                                                                    examples = [ "mike123456@email.com" ] )

class UserProfile( UserBase ):
    
    public_id: UUID

    model_config = ConfigDict(
        json_schema_extra = {
            "examples": [ 
                example[ "created_profile" ]
            ]
        }
        
    )                          