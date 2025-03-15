from typing import Optional
from beanie import Document
from app.models.base import BaseEntity

class UserProfile( BaseEntity, Document ):
    
    name: Optional[ str ] = None
    email: Optional[ str ] = None
    class Settings:
        name = "users"

_example_value = { 
    "name": "Mike",
    "email": "mike123@email.com"
}