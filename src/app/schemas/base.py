import joblib
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class BaseEntity( BaseModel ):
    
    created_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    updated_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )


class SKLearnPredictor( ABC ):

    def __init__( self, model_class ):

        self.model = None
        self.model_class = model_class

    async def load( self, path ):

        classifier = None
        with open( path, "rb" ) as f:
            classifier = joblib.load( f )

        if not isinstance( classifier, self.model_class ):
            raise TypeError( f"Object type error, expected {self.model_class}, but got {type( classifier )}" )

        self.model = classifier
        print( f"{self.model_class} Model loaded successfully" )
        
    def _validate( self, features_df ):

        feature_names = features_df.columns.tolist()
        
        assert self.model is not None, f"failed: Expected LiverDiseasePredictor model is not None"
        assert len( feature_names ) == self.model.n_features_in_, \
                    f"failed: Expected {self.model.n_features_in_} but got {len( feature_names )}"
        
        assert feature_names == self.model.feature_names_in_.tolist()

    @abstractmethod
    def predict( self, features ):
        pass