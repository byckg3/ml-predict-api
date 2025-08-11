import pandas as pd
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.schemas.base import BaseEntity, SKLearnPredictor

example = {
    "created_record": {
        "user_id": "67d1e37bf80ba6a47c3eee61",
        "features": {
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
    },
    "updated_value1": {
        "features.trestbps": 125, 
        "features.target": 0
    },
    "updated_value2": {
        "features.chol": 212, 
        "features.thalach": 168
    }
}

# https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
class HeartDiseaseFeatures( BaseModel ):
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
    target: int | None = None       # the presence of heart disease in the patient, 0 = no disease and 1 = disease

    def set_target( self, result ):
        self.target = result

    def to_df( self, exclude: list[ str ] = [] ):

        features_dict = { "age": self.age, 
                          "sex": self.sex, 
                          "cp": self.cp, 
                          "trestbps": self.trestbps, 
                          "chol": self.chol, 
                          "fbs": self.fbs, 
                          "restecg": self.restecg, 
                          "thalach": self.thalach, 
                          "exang": self.exang, 
                          "oldpeak": self.oldpeak, 
                          "slope": self.slope,
                          "ca": self.ca,
                          "thal": self.thal,
                          "target": self.target }
        
        features_df = pd.DataFrame( features_dict, index = [ 0 ] )
        if exclude:
            features_df.drop( columns = exclude, inplace = True )

        return features_df

class HeartDiseaseRecord( BaseEntity, Document ):
    user_id: PydanticObjectId | None = None
    features: HeartDiseaseFeatures

    class Settings:
        name = "heart-records"

    model_config = {
        "json_schema_extra": {
            "examples": [ example[ "created_record" ] ]
        }
    }

class HeartDiseasePredictor( SKLearnPredictor ):

    def __init__( self, model_class ):
        super().__init__( model_class )

    def predict( self, features: HeartDiseaseFeatures ):

        features_df = features.to_df( exclude = [ "target" ] )
        self._validate( features_df )

        return self.model.predict( features_df )