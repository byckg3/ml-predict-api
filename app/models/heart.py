from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.base import BaseEntity

# https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
class HeartDiseaseRecord( BaseEntity, Document ):
    user_id: Optional[ PydanticObjectId ] = None
    age: int
    sex: int
    cp: int                         # chest pain type ( 4 values )
    trestbps: int                   # resting blood pressure
    chol: int                       # serum cholestoral in mg/dl
    fbs: int                        # fasting blood sugar > 120 mg/dl
    restecg: int                    # resting electrocardiographic results (values 0,1,2)
    thalach: int                    # maximum heart rate achieved
    exang: int = 0                  # exercise induced angina
    oldpeak: float                  # ST depression induced by exercise relative to rest
    slope: int                      # the slope of the peak exercise ST segment
    ca: int                         # number of major vessels (0-3) colored by flourosopy
    thal: int                       # 0 = normal; 1 = fixed defect; 2 = reversable defect
    target: Optional[ int ] = None  # the presence of heart disease in the patient, 0 = no disease and 1 = disease

    class Settings:
        name = "heart-records"

_example_value = {
    "user_id": "67d1e37bf80ba6a47c3eee61",
    "age": 52,
    "sex": 1,
    "cp": 0,
    "trestbps": 125,
    "chol": 212,
    "fbs": 0,
    "restecg": 1,
    "thalach": 168,
    "exang": 0,
    "oldpeak": 1,
    "slope": 2,
    "ca": 2,
    "thal": 3,
    "target": 0
}