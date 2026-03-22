import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from app.db.relational.database import get_async_engine

@pytest.fixture( scope = "module" )
def async_engine() -> AsyncEngine:
    return get_async_engine()


# @pytest.mark.test_only
async def test_postgre_connection( async_engine: AsyncEngine ):
    
    async with async_engine.connect() as conn:
        result = await conn.execute( text( "SELECT 1" ) )
        
        assert result.scalar() == 1, "Failed to execute test query on PostgreSQL database"