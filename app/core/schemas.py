from pydantic import BaseModel, Field
from datetime import datetime, timezone

class BaseDocument( BaseModel ):
    
    created_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    updated_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )