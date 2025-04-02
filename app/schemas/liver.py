import asyncio
import os
import pandas as pd
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from sklearn.ensemble import RandomForestClassifier

from app.schemas.base import BaseEntity, SKLearnPredictor

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
    diagnosis: int | None = None

    def set_target( self, result ):
        self.diagnosis = result

    def to_df( self, exclude: list[ str ] = [] ):

        features_dict = { "Age": self.age, 
                          "Gender": self.gender, 
                          "BMI": self.bmi, 
                          "AlcoholConsumption": self.alcohol_consumption, 
                          "Smoking": self.smoking, 
                          "GeneticRisk": self.genetic_risk, 
                          "PhysicalActivity": self.physical_activity, 
                          "Diabetes": self.diabetes, 
                          "Hypertension": self.hypertension, 
                          "LiverFunctionTest": self.liver_function_test, 
                          "Diagnosis": self.diagnosis }
        
        features_df = pd.DataFrame( features_dict, index = [ 0 ] )
        if exclude:
            features_df.drop( columns = exclude, inplace = True )

        return features_df

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

class LiverDiseasePredictor( SKLearnPredictor ):

    def __init__( self, model_class ):
        super().__init__( model_class )

    def predict( self, features: LiverDiseaseFeatures ):

        features_df = features.to_df( exclude = [ "Diagnosis" ] )
        self._validate( features_df )

        return self.model.predict( features_df )


# python -m app.models.liver
if __name__ == "__main__":
    path = os.getenv( "LIVER_MODEL_URI" )
    classifier = LiverDiseasePredictor( RandomForestClassifier )
    asyncio.run( classifier.load( path ) )
    
    data = pd.read_csv( "D:/jupyter/data/Liver_disease_data.csv" )
    
    input = data.iloc[ 0:1 ].drop( columns = [ "Diagnosis" ] )
    # print( input )
    features = LiverDiseaseFeatures( **example[ "created_record" ][ "features" ]  )
    
    print( "predict:\n", classifier.predict( features ) )