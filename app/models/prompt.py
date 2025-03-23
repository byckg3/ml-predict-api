from beanie import PydanticObjectId
from pydantic import BaseModel

class HealthCareDomain:
    context: str = "堅持在醫療保健的領域內 提供專業又溫暖的建議\n並以簡單明瞭且長話短說的方式回答領域內的提問\n"
    chat_context: str = "可以根據之前的對話內容來回應使用者問題\n"

class HealthCarePrompt( BaseModel ):

    context: str | None = HealthCareDomain.context
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

