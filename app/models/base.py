from datetime import datetime, timezone
from typing import Optional
from beanie import Document, Insert, before_event
from pydantic import BaseModel, Field

class BaseEntity( BaseModel ):
    
    created_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    updated_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )