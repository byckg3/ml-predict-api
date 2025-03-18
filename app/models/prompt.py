from beanie import PydanticObjectId
from pydantic import BaseModel

class Prompt( BaseModel ):

    context: str | None = "請盡量以簡單明瞭並且長話短說的方式回答以下使用者的問題:"
    user_id: PydanticObjectId | None = None
    user_question: str | None = ""

    model_config = {
        "json_schema_extra": {
            "examples": [ 
                { 
                    "user_question": "該如何預防肝臟疾病" 
                },
                { 
                    "user_question": "該如何預防心臟疾病" 
                }
            ]
        }
    }