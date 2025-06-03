from app.services.nosql import DocumentService
from app.schemas.user import UserProfile

class UserProfileService( DocumentService ):

    def __init__( self, user_class: UserProfile ):
        super().__init__( user_class )
        self.user_profile_class = user_class


    async def find_by_email( self, email: str ) -> UserProfile: 

        return await self.repository.find_one( self.user_profile_class.email == email )
    
    
    async def find_or_create_by_email( self, user_info: dict ) -> UserProfile:

        user_email = user_info.get( "email" )
        user_name = user_info.get( "name" )
            
        user_profile = await self.find_by_email( user_email )
        if not user_profile:
            user_profile = await self.repository.save( UserProfile( name = user_name, email = user_email ) )

        return user_profile