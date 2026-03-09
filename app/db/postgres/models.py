from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# avoid circular dependency
class Base( AsyncAttrs, DeclarativeBase ):
    pass


class BaseEntity( Base ):
    __abstract__ = True

    id: Mapped[ int ] = mapped_column( BigInteger, primary_key = True )
   
    created_at: Mapped[ datetime ] = mapped_column( DateTime( timezone = True ), 
                                                    server_default = func.now() )
    
    updated_at: Mapped[ datetime ] = mapped_column( DateTime( timezone = True ), 
                                                    server_default = func.now(), 
                                                    onupdate = func.now() )