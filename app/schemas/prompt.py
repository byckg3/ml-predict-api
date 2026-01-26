import textwrap
from beanie import PydanticObjectId
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from google.genai import types

class HealthCare:
    system_prompt: str = textwrap.dedent( """
    這裡是心肝寶貝の疾病風險預測服務，使用者可以在我們網頁介面輸入生理檢測或生活習慣等相關資料，
    這些資料將作為心臟病和肝病風險預測的基礎
    而你是心肝寶貝的線上健康諮詢小助手，在醫療保健領域內提供使用者專業又溫暖的建議
    當使用者向你提問時，盡量以簡單明瞭且長話短說的方式回答領域內的問題
    使用者可能會持續提問，希望你可以記住之前的對話內容來關心使用者遇到的狀況
    若問到與預測結果相關的提問時，要告訴使用者我們的預測結果僅代表是否有潛在風險，建議使用者要配合醫師診斷以確認健康狀況。
    若遇到不理智或向你挑釁的使用者提問時，請務必堅持你的醫療保健專業，禮貌性地簡單回覆即可，不需隨之起舞。
    如果被詢問到是否可以幫忙評估心臟病風險，請呼叫 predict_heart_risk 函式來評估可能心臟病風險程度。

    以下是你務必要遵守的基本原則:
    1. 參考經過驗證的醫學資料庫 ( 如 UpToDate、PubMed、CDC、WHO )
    2. 確保提供的資訊符合最新的醫學指南 ( 如 ADA、AHA、NICE 指南 )
    3. 明確標示資訊來源，避免誤導
    4. 遵守 HIPAA( 美國健康保險可攜性與責任法案 )或 GDPR( 歐盟一般數據保護法 )，保護使用者隱私
    5. 強調「非診斷用途」，避免誤導使用者自行診斷或治療
    6. 若涉及高風險醫療決策，應建議使用者諮詢醫生
    7. 避免過度自信的回答，可以明確表達不確定性 ( 如「根據目前資料，可能存在多種解釋，建議就醫」)
    8. 提供「風險 vs. 益處」的客觀資訊，而非單方面推薦
    9. 使用淺顯易懂的語言，避免過於專業的術語，若必須使用專業術語，應提供清楚的解釋
    10. 舉例說明，讓使用者更容易理解
    11. 確保醫學建議適用於不同性別、種族、年齡層和健康狀況
    12. 公平提供資訊，避免暗示性別歧視或種族差異 ( 如某些疾病被錯誤地標籤為「只影響某個族群」)
    13. 辨識緊急情況 (如心臟病發作、中風、嚴重過敏反應) 並建議立即就醫
    14. 不對緊急狀況提供遠端診斷，而是直接指導用戶撥打急救電話( 如 119、911 )
    15. 標示高風險症狀，如「若有劇烈胸痛且冒冷汗，請立即就醫」

    以下是你千萬要極力避免的風險:
    1. 可能產生錯誤或過時的資訊，無法取代專業醫生的臨床判斷
    2. 若洩露個人醫療資訊，可能違反醫療隱私法規
    3. 若提供錯誤或危險的建議，可能引發法律責任
    4. 表現得過於確定，可能讓使用者錯誤信任結果
    5. 可能無法充分考慮個人病史、檢查結果或藥物交互作用
    6. 若未能識別緊急情況，可能導致錯過黃金治療時間
    7. 若錯誤建議使用者自行處理，可能導致生命危險
    """ )
    
    chat_template: str = textwrap.dedent( """
    以下是已檢索到相關的問答資料，可供參考:
    {retrieved_content}
                                         
    以下是已檢索到相關文件的段落，可供參考:
    {retrieved_document}                                    

    若檢索到的資料有缺失空白或與使用者的問題不相關，則可忽略這些資料。
    若檢索到的資訊不足，請避免編造資訊。
    
    以下是你要回應的使用者提問：
    {user_query}

    記住之前的對話內容來回應使用者問題
    若你需要更多資訊來提供準確建議，請主動詢問使用者。\n
    """ )
    
    # Define the function declaration for the model
    function_declarations = {
        "predict_heart_risk": {
            "name": "predict_heart_risk",
            "description": "當使用者要求評估心臟疾病風險時，請呼叫此函式。結果 0 代表無風險，1 代表有一定程度的風險",
            "parameters": {
                "type": "object",
                "properties": {
                    "age": {
                        "type": types.Type.INTEGER,
                        "description": "年齡",
                    },
                    "sex": {
                        "type": types.Type.INTEGER,
                        "description": "性別，0 表示女性，1 表示男性",
                    },
                    "cp": {
                        "type": types.Type.INTEGER,
                        "description": "胸痛類型，0 表示無胸痛，1 = 典型心絞痛；2 = 非典型心絞痛；3 = 非心絞痛；4 = 無症狀性胸痛",
                    },
                    "trestbps": {
                        "type": types.Type.INTEGER,
                        "description": "靜息血壓( 以 mm Hg 為單位 )",
                    },
                    "chol": {
                        "type": types.Type.INTEGER,
                        "description": "血清膽固醇，單位 mg/dl( 血液膽固醇濃度 )",
                    },
                    "fbs": { 
                        "type": types.Type.INTEGER,
                        "description": "空腹血糖是否 > 120 mg/dl，1 表示 true，0 表示 false",
                    },
                    "restecg": {
                        "type": types.Type.INTEGER,
                        "description": "靜息心電圖結果，0 = 正常；1 = 有 ST-T 波異常；2 = 顯示可能或確定的左心室肥大",
                    },
                    "thalach": {
                        "type": types.Type.INTEGER,
                        "description": "運動或測試中達到的最大心跳率",
                    },
                    "exang": {
                        "type": types.Type.INTEGER,
                        "description": "運動誘發的心絞痛，1 表示有，0 表示無",
                    },
                    "oldpeak": {
                        "type": types.Type.NUMBER,
                        "description": "運動相比於休息狀態所引起的 ST 段壓低程度",
                    },
                    "slope": {
                        "type": types.Type.INTEGER,
                        "description": "ST 段峰值斜率，1 = 上坡；2 = 平緩；3 = 下坡( 最高運動 ST 段的斜率 )",
                    },
                    "ca": {
                        "type": types.Type.INTEGER,
                        "description": "螢光染色後顯示的主要血管數量( 0-3 )",
                    },
                    "thal": {
                        "type": types.Type.INTEGER,
                        "description": "心血管造影結果類別，0 = 正常；1 = 固定缺陷；2 = 可逆缺陷",
                    },
                },
                "required": [ "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal" ],
            },
        }
    }

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