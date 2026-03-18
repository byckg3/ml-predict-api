import pytest
from typing import Any
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from app.user.models import User
from app.user.schemas import example
from app.user.repositories.impl import UserRepository

# @pytest.mark.test_only
class TestUserRepository:
    
    @pytest.fixture( scope = "class" )
    async def test_user( self ):
        user_data: dict[ Any, Any ] = example[ "created_profile" ]
        return User( **user_data )
    
    
    async def test_crud_user( self, async_session_factory: async_sessionmaker[ AsyncSession ], test_user: User ):
        
        async with async_session_factory() as session:
            user_repository = UserRepository( session )
            
            # save
            user = await user_repository.save( test_user )
            await session.flush()
            # print( f"Saved user:\n{user}" )
            assert user.id is not None
            assert user.public_id is not None
            assert user.created_at is not None
            
            user_public_id = str( user.public_id )
            
            
            # update
            updated_name = "New Name"
            updated_user = await user_repository.update_by_public_id( user_public_id, { "name": updated_name } )
            await session.flush()                  # Synchronize changes to the DB
            await session.refresh( updated_user )  # Fetch the latest values from the DB
            # print( f"Updated user:\n{updated_user}" )
            
            
            # find by public_id
            queried_user = await user_repository.find_by_public_id( user_public_id )
            # print( f"Queried user:\n{queried_user}" )
            assert queried_user is not None
            assert queried_user.id == user.id
            assert queried_user.name == updated_name
            
            
            # delete by id
            deleted_count = await user_repository.delete_by_public_id( user_public_id )
            assert deleted_count == 1


            # find all
            all_users = await user_repository.find_all()
            assert len( all_users ) == 0
            
            
            await session.rollback()
            
    
    async def test_delete_users( self, async_session_factory: async_sessionmaker[ AsyncSession ], test_user: User ):
        
        async with async_session_factory() as session:
            user_repository = UserRepository( session )
            
            # save a user
            new_user = await user_repository.save( test_user )
            await session.flush()
            
            # delete user
            await user_repository.delete( new_user )
            await session.flush()
            
            
            # delete all users
            deleted_count = await user_repository.delete_all()
            # print( f"Deleted { deleted_count } users" )
            assert deleted_count == 0
            
            
            await session.rollback()