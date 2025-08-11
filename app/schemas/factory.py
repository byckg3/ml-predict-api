import asyncio
import os
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier

from app.schemas.heart import HeartDiseasePredictor
from app.schemas.liver import LiverDiseaseFeatures, LiverDiseasePredictor, example


class DiseasePredictorFactory:

    _model_registry = {
        "heart": {
            "sklearn/random_forest": RandomForestClassifier
        },
        "liver": {
            "sklearn/random_forest": RandomForestClassifier,
            "sklearn/gradient_boosting": GradientBoostingClassifier,
        }
    }

    _pre_processor = {
        "heart": None,
        "liver": None
    }

    _wrapper = {
        "heart": HeartDiseasePredictor,
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