from app.schemas.factory import DiseasePredictorFactory
from app.schemas.liver import LiverDiseasePredictor


def test_factory_create_predictor_successfully():
    
    predictor = DiseasePredictorFactory.create_disease_predictor( "liver", "sklearn/random_forest" )

    assert isinstance( predictor, LiverDiseasePredictor ) == True