from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.postgres.models import Base, IdMixin, TimestampMixin

example = {
    "login_info": {
        "email": f"mike123456@email.com"
    },
    "created_profile": {
        "name": "Mike",
        "email": f"mike{ int( datetime.now().timestamp() ) }@email.com"
    }
}

class User( IdMixin, TimestampMixin, Base ):
    __tablename__ = "users"

    public_id: Mapped[ UUID ] = mapped_column( default = uuid4, unique = True )
    email: Mapped[ str ] = mapped_column( String( 50 ), nullable = False, unique = True )
    name: Mapped[ str | None ] = mapped_column( String( 20 ), default = "unknown", nullable = True )
    
    
    def __repr__( self ):
        data = {
            "id": self.id,
            "public_id": self.public_id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        return data.__repr__()
    
    __str__ = __repr__