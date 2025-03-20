import os
import joblib
import numpy as np
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier

from app.models.liver import LiverDiseaseFeatures, example

class LiverDiseaseClassifier:

    def __init__( self, model_class, path ):

        self.model = None
        self.model_class = model_class
        self.load( path )

    def load( self, path ):

        classifier = None
        with open( path, "rb" ) as f:
            classifier = joblib.load( f )

        if isinstance( classifier, self.model_class ):
            self.model = classifier
            print( "Model loaded successfully" )
        else:
            print( type( classifier ) )
            raise TypeError( f"Object type error, expected {self.model_class}, but got {type( classifier )}" )

    def predict( self, features: LiverDiseaseFeatures ):

        features_df = features.to_df( exclude = [ "Diagnosis" ] )
        print( features_df )
        return self.model.predict( features_df )


# python app\models\ml\sk.py
if __name__ == "__main__":
    path = os.getenv( "LIVER_MODEL_URI" )
    classifier = LiverDiseaseClassifier( RandomForestClassifier, path )
    print( classifier.model.n_features_in_ )
    print( classifier.model.feature_names_in_ )

    import pandas as pd

    data = pd.read_csv( "D:/jupyter/data/Liver_disease_data.csv" )
    print( data.head() )
    input = data.iloc[ 0:1 ].drop( columns = [ "Diagnosis" ] )
    print( input )

    print( "predict:\n", classifier.model.predict( input ) )

    features = LiverDiseaseFeatures( **example[ "created_record" ][ "features" ]  )
    print( features )
    print( "predict:\n", classifier.predict( features ) )