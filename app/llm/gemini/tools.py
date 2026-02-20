from google.genai import types

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