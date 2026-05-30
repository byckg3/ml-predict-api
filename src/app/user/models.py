from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.relational.models import Base, IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.heart_disease.models import HeartDiseaseRecord

class User( IdMixin, TimestampMixin, Base ):
    __tablename__ = "users"

    public_id: Mapped[ UUID ] = mapped_column( default = uuid4, unique = True )
    email: Mapped[ str ] = mapped_column( String( 50 ), nullable = False, unique = True )
    name: Mapped[ str | None ] = mapped_column( String( 20 ), default = "unknown", nullable = True )

    heart_disease_records: Mapped[ list[ "HeartDiseaseRecord" ] ] = relationship(
        back_populates = "owner",
        lazy = "raise",
        cascade = "all, delete-orphan"
    )

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