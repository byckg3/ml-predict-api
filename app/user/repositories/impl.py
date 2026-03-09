from typing import Any
from sqlalchemy import CursorResult, Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.models import User


class UserRepository:
    
    def __init__( self, async_session: AsyncSession ):
        self._async_session = async_session
        
        
    def save_user( self, user: User ) -> User:
        self._async_session.add( user )
               
        return user
    
    
    async def get_by_public_id( self, id: str ) -> User | None:
        stmt = select( User ).where( User.public_id == id )
        
        return await self._async_session.scalar( stmt )
    
    
    async def get_all( self, limit: int = 10, offset: int = 0 ) -> list[ User ]:
        stmt = select( User ).limit( limit ).offset( offset )
        result = await self._async_session.execute( stmt )
        
        return list( result.scalars().all() )
    
    
    async def update_by_public_id( self, id: str, patch: dict ) -> User | None:
        user = await self.get_by_public_id( id )
        
        if user:
            for key, value in patch.items():
                setattr( user, key, value )
        
        return user
    
    
    async def delete_user( self, user: User ):
        await self._async_session.delete( user )
    
    
    async def delete_by_public_id( self, id ):
        stmt = delete( User ).where( User.public_id == id )
        result: Result = await self._async_session.execute( stmt )
        
        if isinstance( result, CursorResult ):
            return result.rowcount
        
        return 0
    
    
    async def delete_all( self ) -> int:
        stmt = delete( User )
        result: Result = await self._async_session.execute( stmt )
        
        if isinstance( result, CursorResult ):
            return result.rowcount
        
        return 0