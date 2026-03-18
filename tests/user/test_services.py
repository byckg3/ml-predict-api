
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from app.user.models import User
from app.user.v2.schemas import example
from app.user.services import UserService

@pytest.mark.test_only
class TestUserService:
    
    @pytest.fixture( scope = "class" )
    async def test_user( self ):
        user_data: dict = example[ "created_profile" ]
        return User( **user_data )
    
    
    @pytest.fixture( scope = "class" )
    async def user_service( self, async_session_factory: async_sessionmaker[ AsyncSession ] ):
        
        user_service = UserService( async_session_factory )
        yield user_service
        
        deleted_count = await user_service.delete_all()
        print( f"Deleted { deleted_count } users in teardown" )
    
    
    async def test_save_user( self, user_service: UserService, test_user: User ):
        
        saved_user = await user_service.save( test_user )
        # print( f"Saved user:\n{saved_user}" )
        
        assert saved_user.id is not None
        assert saved_user.public_id is not None
        assert saved_user.created_at is not None
        
    
    async def test_find_all_users( self, user_service: UserService, test_user: User ):
        
        users = await user_service.find_all()
        # print( f"Found users:\n{users}" )
        
        assert len( users ) == 1
        assert users[ 0 ].id == test_user.id
        
        
    async def test_update_user( self, user_service: UserService, test_user: User ):
        
        id = str( test_user.public_id )
        updated_name = "Updated Name"
        updated_user = await user_service.update_by_id( id, { "name": updated_name } )
        # print( f"Updated user:\n{updated_user}" )
        
        assert updated_user is not None
        assert updated_user.name == updated_name
        assert updated_user.updated_at > updated_user.created_at
        
        
    async def test_find_user_by_id( self, user_service: UserService, test_user: User ):
        
        id = str( test_user.public_id )
        queried_user = await user_service.find_by_id( id )
        # print( f"Queried user:\n{queried_user}" )
        
        assert queried_user is not None
        assert queried_user.id == test_user.id
        assert str( queried_user.public_id ) == id
        
    
    async def test_delete_user_by_id( self, user_service: UserService, test_user: User ):
        
        id = str( test_user.public_id )
        deleted_count = await user_service.delete_by_id( id )
        
        assert deleted_count == 1
        
        # Verify deletion
        queried_user = await user_service.find_by_id( id )
        assert queried_user is None