import pytest
from typing import Any
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from app.db.postgres.connection import get_engine, get_session_factory, init_tables
from app.user.models import User, example
from app.user.repositories.impl import UserRepository

@pytest.mark.test_only
class TestUserRepository:
    
    @pytest.fixture( scope = "class" )
    async def async_session_factory( self ) :
        async_engine = get_engine( env = "test" )
        await init_tables( async_engine, [ User ] )
        
        yield get_session_factory( async_engine )
        
        await async_engine.dispose()

    
    @pytest.fixture( scope = "class" )
    async def test_user( self ):
        user_data: dict[ Any, Any ] = example[ "created_profile" ]
        return User( **user_data )
    
    
    async def test_crud_user( self, async_session_factory: async_sessionmaker[ AsyncSession ], test_user: User ):
        
        async with async_session_factory() as session:
            user_repository = UserRepository( session )
            
            # save
            user = user_repository.save_user( test_user )
            await session.flush()
            # print( f"User saved with ID: {user.id}" )
            # print( user )
            assert user.id is not None
            assert user.public_id is not None
            assert user.created_at is not None
            
            user_public_id = str( user.public_id )
            
            # update user
            updated_name = "New Name"
            await user_repository.update_by_public_id( user_public_id, { "name": updated_name } )
            await session.flush()
            
            
            #  get by public_id
            queried_user = await user_repository.get_by_public_id( user_public_id )
            # await session.flush()
            # print( f"Queried user: {queried_user}" )
            assert queried_user is not None
            assert queried_user.id == user.id
            assert queried_user.name == updated_name
            
            
            # delete by id
            deleted_count = await user_repository.delete_by_public_id( user_public_id )
            assert deleted_count == 1


            # get all users
            all_users = await user_repository.get_all()
            assert len( all_users ) == 0
            
            
            await session.rollback()
            
    
    async def test_delete_users( self, async_session_factory: async_sessionmaker[ AsyncSession ], test_user: User ):
        
        async with async_session_factory() as session:
            user_repository = UserRepository( session )
            
            # save a user
            new_user = user_repository.save_user( test_user )
            await session.flush()
            
            
            # delete user
            await user_repository.delete_user( new_user )
            await session.flush()
            
            
            # delete all users
            deleted_count = await user_repository.delete_all()
            # print( f"Deleted { deleted_count } users" )
            assert deleted_count == 0
            
            
            await session.rollback()