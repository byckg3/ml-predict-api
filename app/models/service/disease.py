import asyncio
from typing import overload
from app.config.settings import hf_settings
from app.models.factory import DiseasePredictorFactory
from app.models.heart import HeartDiseaseFeatures
from app.models.liver import LiverDiseaseFeatures, LiverDiseasePredictor
from app.models.repository import HFModelRepository


class DiseasePredictionService:

    def __init__( self ):      
        
        self.liver_predictor = DiseasePredictorFactory.create_disease_predictor( "liver", hf_settings().liver_classifier )
        self.heart_predictor = DiseasePredictorFactory.create_disease_predictor( "heart", hf_settings().heart_classifier )
        self.hf_repository = HFModelRepository()

    async def models_init( self ):
        
        liver_model_path = await self.hf_repository.download( hf_settings().liver_model_uri )
        await self.liver_predictor.load( liver_model_path )

        heart_model_path = await self.hf_repository.download( hf_settings().heart_model_uri )
        await self.heart_predictor.load( heart_model_path )

        print( f"DiseasePredictionService init models successfully" )
    
    @overload
    def predict( self, features: HeartDiseaseFeatures ):
        ...

    def predict( self, features: LiverDiseaseFeatures ):

        result = None
        if isinstance( features, LiverDiseaseFeatures ):   
            result = self.liver_predictor.predict( features )
        
        elif isinstance( features, HeartDiseaseFeatures ):
            result = self.heart_predictor.predict( features )

        features.set_target( int( result[ 0 ] ) )
        
        return features

# python -m app.models.service.disease
if __name__ == "__main__":
    service = DiseasePredictionService()
    asyncio.run( service.models_init() ) 
    assert service.liver_predictor.model is not None