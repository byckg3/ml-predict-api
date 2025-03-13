from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

# https://www.kaggle.com/datasets/rabieelkharoua/predict-liver-disease-1700-records-dataset
class LiverDiseaseRecord( Document ):
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

    class Settings:
        name = "liver-records"