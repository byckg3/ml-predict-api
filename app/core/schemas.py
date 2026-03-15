from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone

class Base( BaseModel ):
    
    created_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    updated_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    
    model_config = ConfigDict( 
        from_attributes=True,
        extra = "ignore" 
    )