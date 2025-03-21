from typing import overload
from app.models.heart import HeartDiseaseFeatures
from app.models.liver import LiverDiseaseFeatures, LiverDiseasePredictor


class DiseasePredictionService:

    def __init__( self, heart = None, 
                        liver: LiverDiseasePredictor = None ):      
         
        self.liver_predictor = liver
        self.heart_predictor = heart

    @overload
    async def predict( self, features: LiverDiseaseFeatures ):
        return await self.liver_predictor.predict( features )
    
    @overload
    async def predict( self, features: HeartDiseaseFeatures ):
        return await self.heart_predictor.predict( features )