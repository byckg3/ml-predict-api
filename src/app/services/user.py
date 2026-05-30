from typing import Type
from app.services.nosql import DocumentService
from app.user.v1.schemas import UserProfile

class UserProfileService( DocumentService[ UserProfile ] ):

    def __init__( self, user_class: Type[ UserProfile ] ):
        super().__init__( user_class )
        self.user_profile_class = user_class


    async def find_by_email( self, email: str ) -> UserProfile | None: 

        return await self.repository.find_one( self.user_profile_class.email == email )
    
    
    async def find_or_create_by_email( self, user_info: dict ) -> UserProfile:

        user_email = user_info.get( "email" )
        user_name = user_info.get( "name" )
        if not user_email:
            raise ValueError( "Email is required to find or create user profile" )
            
        user_profile = await self.find_by_email( user_email )
        if not user_profile:
            user_profile = await self.repository.save( UserProfile( name = user_name, email = user_email ) )

        return user_profile