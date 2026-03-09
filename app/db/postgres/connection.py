import re
import asyncio
from typing import Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import Table

from app.core.config import ENV, postgre_settings
from app.db.postgres.models import Base

def get_engine( env: str = ENV ) -> AsyncEngine:
    if env == "test":
        db_url = postgre_settings().TEST_DB_URL
    else:
        db_url = postgre_settings().DATABASE_URL
    
    print( f"PostgreSQL URI: {db_url}" )
        
    return create_async_engine( re.sub( r'^postgresql:', "postgresql+asyncpg:", db_url ), echo = True )


def get_session_factory( async_engine: AsyncEngine ) -> async_sessionmaker[ AsyncSession ]:
    return async_sessionmaker( async_engine, expire_on_commit = False )


M = TypeVar( "M", bound = Base )
async def init_tables( async_engine: AsyncEngine, model_types: list[ Type[ M ] ] | None = None ):
    
    async with async_engine.begin() as async_conn:
        
        if model_types:
            
            tables: list[ Table ] = []
            for model in model_types:
                if hasattr( model, "__table__" ) and isinstance( model.__table__, Table ):
                    tables.append( model.__table__ )
            
            await async_conn.run_sync(
                lambda sync_conn: Base.metadata.create_all(
                    bind = sync_conn,
                    tables = tables
                )
            )
            
        else:
            await async_conn.run_sync( Base.metadata.create_all )
    
    
# python -m app.dbs.postgre
if __name__ == "__main__":
    async_engine = get_engine()
    asyncio.run( init_tables( async_engine ) )