from fastapi import APIRouter
from app.models.dataset import MedicalRecord

router = APIRouter( prefix="/heart" )

@router.get( "/records", response_model = list[ MedicalRecord ] )
def get_records():

    new_record = MedicalRecord( age = 45, 
                                sex = 1, 
                                cp = 3, 
                                trestbps = 120,
                                chol = 233, 
                                fbs = 0,
                                restecg = 1, 
                                thalach = 170, 
                                exang = 0, 
                                oldpeak = 2.3,
                                slope = 2, 
                                ca = 0, 
                                thal = 2 )

    return [ new_record ]


@router.post( "/predict" )
async def predict_target( record: MedicalRecord ):

    try:
        print( record )
        record.age = 99
        record.target = 1
        
        return { "result": record }
    
    except Exception as e:
        print( e )
        return { "error": "An error occurred" }
    
    