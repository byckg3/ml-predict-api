from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.base import BaseEntity

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

# https://www.kaggle.com/datasets/rabieelkharoua/predict-liver-disease-1700-records-dataset
class LiverDiseaseFeatures( BaseModel ):
    age: int
    gender: int                 = Field( ge = 0, le = 1 )
    bmi: float
    alcohol_consumption: float
    smoking: int                = Field( ge = 0, le = 1 )
    genetic_risk: int           = Field( ge = 0, le = 2 )
    physical_activity: float
    diabetes: int               = Field( ge = 0, le = 1 )
    hypertension: int           = Field( ge = 0, le = 1 )
    liver_function_test: float
    diagnosis: int | None
    
class LiverDiseaseRecord( BaseEntity, Document ):
    user_id: PydanticObjectId | None = None
    features: LiverDiseaseFeatures

    class Settings:
        name = "liver-records"

    model_config = {
        "json_schema_extra": {
            "examples": [ example[ "created_record" ] ]
        }
    }