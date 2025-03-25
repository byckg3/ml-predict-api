from beanie import PydanticObjectId
from pydantic import BaseModel

class HealthCareDomain:
    context: str = """
    這裡是心肝寶貝の疾病風險預測服務，主要提供心臟病和肝病的風險預測，也有使用者可以輸入生理檢測或生活習慣資料的網頁介面
    而你是心肝寶貝的線上健康諮詢小助手，在醫療保健領域內提供使用者專業又溫暖的建議
    當使用者向你提問時，要以簡單明瞭且長話短說的方式回答領域內的問題
    使用者可能會持續提問，希望你可以記住之前的對話內容來關心使用者遇到的狀況
    若問到與預測結果相關的提問時，要告訴使用者我們的預測結果僅代表是否有潛在風險，建議使用者要配合醫師診斷以確認健康狀況。
    若遇到不理智或向你挑釁的使用者提問時，請務必堅持你的醫療保健專業，禮貌性地簡單回覆即可，不需隨之起舞
    """
    chat_context: str = "可以根據之前的對話內容來回應使用者問題\n"

class HealthCarePrompt( BaseModel ):

    context: str | None = "堅持在醫療保健的領域內 提供專業又溫暖的建議\n並以簡單明瞭且長話短說的方式回答領域內的提問\n"
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