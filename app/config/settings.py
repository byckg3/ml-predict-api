import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

if os.path.exists( ".env" ):
    from dotenv import load_dotenv
    load_dotenv()

class DBSettings( BaseSettings ):

    MONGO_URI: str
    DB_NAME: str

    model_config = SettingsConfigDict( env_file = ".env", extra = "ignore" )

class HuggingFaceSettings( BaseSettings ):

    HF_TOKEN: str
    REPOSITORY_ID: str

    liver_classifier: str = "sklearn/gradient_boosting"
    liver_model_uri: str = f"liver/{liver_classifier}/01/model.pkl"

    heart_classifier: str = "sklearn/random_forest"
    heart_model_uri: str = f"heart/{heart_classifier}/01/model.pkl"

    model_config = SettingsConfigDict( env_file = ".env", extra = "ignore" )


class GeminiAPISettings( BaseSettings ):

    GEMINI_API_KEY: str
    TUNED_MODEL_ID: str

    model_config = SettingsConfigDict( env_file = ".env", extra = "ignore" )




@lru_cache()
def db_settings():
    return DBSettings()

@lru_cache()
def hf_settings():
    return HuggingFaceSettings()

@lru_cache()
def gemini_settings():
    return GeminiAPISettings()


# python -m app.config.settings
if __name__ == "__main__":
    settings = hf_settings()
    print( settings )