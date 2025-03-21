from app.models.factory import DiseasePredictorFactory
from app.models.liver import LiverDiseasePredictor


def test_factory_create_predictor_successfully():
    
    predictor = DiseasePredictorFactory.create_disease_predictor( "liver", "random_forest" )

    assert isinstance( predictor, LiverDiseasePredictor ) == True