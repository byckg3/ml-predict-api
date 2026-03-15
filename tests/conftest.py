import pytest

from app.core.db import MongoDB
from app.db.postgres.connection import get_engine, get_session_factory, init_tables
from app.user.models import User

# Possible values for scope are: function, class, module, package or session
@pytest.fixture( scope = "session" )
def anyio_backend():
    return "asyncio"


@pytest.fixture( scope = "session" )
async def setup_mongo( anyio_backend ):
    MongoDB.DB_NAME = "test"
    monogo = MongoDB()
    await monogo.init_beanie()

    yield

    await monogo.close()
    

@pytest.fixture( scope = "session" )
async def async_session_factory() :
    async_engine = get_engine( env = "test" )
    await init_tables( async_engine, [ User ] )
    
    yield get_session_factory( async_engine )
    
    await async_engine.dispose()