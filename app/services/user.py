from app.services.nosql import DocumentService
from app.models.user import UserProfile

class UserProfileService( DocumentService ):

    def __init__( self, user_class: UserProfile ):
        super().__init__( user_class )
        self.user_profile_class = user_class

    async def find_by_email( self, email: str ): 
        return await self.repository.find_one( self.user_profile_class.email == email )