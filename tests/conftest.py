import pytest

from app.core.db import MongoDB

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