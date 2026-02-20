from fastapi import Depends, Request
from app.llm.gemini.services import ChatService
from app.schemas.heart import HeartDiseaseRecord
from app.schemas.liver import LiverDiseaseRecord
from app.schemas.user import UserProfile
from app.services.nosql import RecordService
from app.services.disease import DiseasePredictionService
from app.services.user import UserProfileService

def heart_record_service( request: Request ) -> RecordService:

    if not hasattr( request.app.state, "heart_record_service" ):
        request.app.state.heart_record_service = RecordService( HeartDiseaseRecord )

    return request.app.state.heart_record_service


def liver_record_service( request: Request ) -> RecordService:

    if not hasattr( request.app.state, "liver_record_service" ):
        request.app.state.liver_record_service = RecordService( LiverDiseaseRecord )

    return request.app.state.liver_record_service


def user_profile_service( request: Request ) -> UserProfileService:

    if not hasattr( request.app.state, "user_profile_service" ):
        request.app.state.user_profile_service = UserProfileService( UserProfile )
        
    return request.app.state.user_profile_service


def predict_service( request: Request ) -> DiseasePredictionService:

    return request.app.state.predict_service


def chat_service( request: Request, predict_service = Depends( predict_service ) ) -> ChatService:

    if not hasattr( request.app.state, "chat_service" ):
        request.app.state.chat_service = ChatService( predict_service)

    return request.app.state.chat_service