from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from app.user.models import User
from app.user.repositories.impl import UserRepository

class UserService:
    
    def __init__( self, async_session_factory: async_sessionmaker[ AsyncSession ] ):
        self._async_session_factory = async_session_factory
        
        
    async def save( self, user ):
        try:
            async with self._async_session_factory() as session:
                async with session.begin():
                    
                    user_repository = UserRepository( session )
                    user = await user_repository.save( user )
                     
            return user
            
        except Exception as e:
            print( f"Error in save: { e }" )
            raise e
        
        
    async def find_by_id( self, id: str ) -> User | None:
        try:
            async with self._async_session_factory() as session:
                async with session.begin():
                    
                    user_repository = UserRepository( session )
                    user = await user_repository.find_by_public_id( id )
            
            return user
            
        except Exception as e:
            print( f"Error in find_by_id: { e }" )
            raise e
        
        
    async def find_all( self, limit: int = 10, offset: int = 0 ) -> list[ User ]:
        try:
            async with self._async_session_factory() as session:
                async with session.begin():
                    
                    user_repository = UserRepository( session )
                    users = await user_repository.find_all( limit, offset )
            
            return users
            
        except Exception as e:
            print( f"Error in find_all: { e }" )
            raise e
        
        
    async def update_by_id( self, id: str, patch: dict ) -> User | None:
        try:
            async with self._async_session_factory() as session:
                async with session.begin():
                    
                    user_repository = UserRepository( session )
                    user = await user_repository.update_by_public_id( id, patch )
                    
                await session.refresh( user )
                
            return user
            
        except Exception as e:
            print( f"Error in update_by_id: { e }" )
            raise e
        
    
    async def delete_by_id( self, id: str ) -> int:
        try:
            async with self._async_session_factory() as session:
                async with session.begin():
                    
                    user_repository = UserRepository( session )
                    deleted_count = await user_repository.delete_by_public_id( id )
            
            return deleted_count
            
        except Exception as e:
            print( f"Error in delete_by_id: { e }" )
            raise e
    
    async def delete_all( self ) -> int:
        try:
            async with self._async_session_factory() as session:
                async with session.begin():
                    
                    user_repository = UserRepository( session )
                    deleted_count = await user_repository.delete_all()
            
            return deleted_count
            
        except Exception as e:
            print( f"Error in delete_all: { e }" )
            raise e