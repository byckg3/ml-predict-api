from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone

class BaseSchema( BaseModel ):
    
    model_config = ConfigDict( 
        from_attributes = True,
        str_strip_whitespace = True,
        extra = "ignore" 
    )
    
class TimestampSchema:
    
    created_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    updated_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )