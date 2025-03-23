from fastapi import Request

from app.models.heart import HeartDiseaseRecord
from app.models.liver import LiverDiseaseRecord
from app.models.service.ai import WSChatManager
from app.models.service.base import RecordService
from app.models.service.disease import DiseasePredictionService

def heart_record_service( request: Request ) -> RecordService:

    if not hasattr( request.app.state, "heart_record_service" ):
        request.app.state.heart_record_service = RecordService( HeartDiseaseRecord )

    return request.app.state.heart_record_service


def liver_record_service( request: Request ) -> RecordService:

    if not hasattr( request.app.state, "liver_record_service" ):
        request.app.state.liver_record_service = RecordService( LiverDiseaseRecord )

    return request.app.state.liver_record_service


def predict_service( request: Request ) -> DiseasePredictionService:

    return request.app.state.predict_service