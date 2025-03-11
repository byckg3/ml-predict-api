from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

# https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
class HeartHealthMetrics( BaseModel ):
    id: Optional[ str ] = None
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


# https://www.kaggle.com/datasets/rabieelkharoua/predict-liver-disease-1700-records-dataset
class LiverHealthMetrics( Document ):
    id:  Optional[ ObjectId ] = Field( alias="_id" )
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
    diagnosis: int