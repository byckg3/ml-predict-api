from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.base import BaseEntity

# https://www.kaggle.com/datasets/rabieelkharoua/predict-liver-disease-1700-records-dataset
class LiverDiseaseFeatures( BaseModel ):
    age: int
    gender: int
    bmi: float
    alcohol_consumption: float
    smoking: int
    genetic_risk: int
    physical_activity: float
    diabetes: int
    hypertension: int
    liver_function_test: float
    diagnosis: Optional[ int ] = None

class LiverDiseaseRecord( BaseEntity, Document ):
    user_id: Optional[ PydanticObjectId ] = None
    features: LiverDiseaseFeatures

    class Settings:
        name = "liver-records"

example = {
    "created_record": { 
        "user_id": "67d1e37bf80ba6a47c3eee61",
        "features": {
            "age": 58,
            "gender": 0,
            "bmi": 35.8,
            "alcohol_consumption": 17.2,
            "smoking": 0,
            "genetic_risk": 1,
            "physical_activity": 0.658,
            "diabetes": 0,
            "hypertension": 0,
            "liver_function_test": 42.73,
            "diagnosis": 1 
        }
    },
    "updated_value1": {
        "features.alcohol_consumption": 18.2,
        "features.smoking": 1
    },
    "updated_value2": {
        "features.genetic_risk": 1,
        "features.physical_activity": 0.658
    }
}