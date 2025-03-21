import asyncio
import os
from sklearn.ensemble import RandomForestClassifier

from app.models.liver import LiverDiseaseFeatures, LiverDiseasePredictor, example


class DiseasePredictorFactory:

    _model_registry = {
        "heart": {

        },
        "liver": {
            "random_forest": RandomForestClassifier
        }
    }

    _pre_processor = {
        "heart": None,
        "liver": None
    }

    _wrapper = {
        "heart": None,
        "liver": LiverDiseasePredictor
    }


    @classmethod
    def create_disease_predictor( cls, disease_name, classifier_type ):
        classifier_cls = cls._model_registry[ disease_name ][ classifier_type ]
        predictor_cls = cls._wrapper[ disease_name ]
        predictor_instance = predictor_cls( classifier_cls )

        return predictor_instance

# python -m app.models.factory
if __name__ == "__main__":

    instance = DiseasePredictorFactory.create_disease_predictor( "liver", "random_forest" )

    path = os.getenv( "LIVER_MODEL_URI" )
    
    asyncio.run( instance.load( path ) )

    features = LiverDiseaseFeatures( **example[ "created_record" ][ "features" ]  )
    
    print( "predict:\n", instance.predict( features ) )