import os
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

if os.path.exists( ".env" ):
    from dotenv import load_dotenv
    load_dotenv()
    
ENV = os.getenv( "ENV", "" )

env_file = ".env"
if ENV:
    env_file = f".env.{ENV}"

class MongoDBSettings( BaseSettings ):

    MONGO_URI: str
    DB_NAME: str

    model_config = SettingsConfigDict( extra = "ignore" )
    
    
class PostgreSQLSettings( BaseSettings ):

    DATABASE_URL: str
    TEST_DB_URL: str = ""

    model_config = SettingsConfigDict( extra = "ignore" )

class ChromaSettings( BaseSettings ):

    CHROMA_DB_COLLECTION: str = "gad245-g1-chromadb-embedding"
    CHROMA_DB_DIR: str = "./chroma"
    CHROMA_DB_PERSISTENT: bool = False

    model_config = SettingsConfigDict( extra = "ignore" )

class HuggingFaceSettings( BaseSettings ):

    HF_TOKEN: str
    HF_REPOSITORY_ID: str

    liver_classifier: str = "sklearn/gradient_boosting"
    liver_model_uri: str = f"liver/{liver_classifier}/01/model.pkl"

    heart_classifier: str = "sklearn/random_forest"
    heart_model_uri: str = f"heart/{heart_classifier}/01/model.pkl"

    model_config = SettingsConfigDict( extra = "ignore" )


class GeminiAPISettings( BaseSettings ):

    API_KEY: str
    MODEL_NAME: str
    EMBEDDING_MODEL_NAME: str
    # TUNED_MODEL_ID: str

    model_config = SettingsConfigDict( 
        env_file_encoding = "utf-8",
        env_prefix = "GEMINI_",
        extra = "ignore",
    )


class GoogleAuthSettings( BaseSettings ):

    CLIENT_ID: str = Field( validation_alias = "GOOGLE_CLIENT_ID" )
    CLIENT_SECRET: str = Field( validation_alias = "GOOGLE_CLIENT_SECRET" )

    model_config = SettingsConfigDict( extra = "ignore" )

class WebSettings( BaseSettings ):

    FRONTEND_URL: str = "http://127.0.0.1:7860"
    BACKEND_URL: str = "http://127.0.0.1:7860"
    SESSION_SECRET: str
    JWT_SECRET: str

    model_config = SettingsConfigDict( extra = "ignore" )



@lru_cache()
def mongo_settings():
    return MongoDBSettings() # type: ignore

@lru_cache()
def postgre_settings():
    return PostgreSQLSettings() # type: ignore

@lru_cache()
def chroma_settings():
    return ChromaSettings()

@lru_cache()
def hf_settings():
    return HuggingFaceSettings() # type: ignore

@lru_cache()
def gemini_settings():
    settings = GeminiAPISettings() # type: ignore
    # print( f"Gemini API settings:\n{settings}" )
    return settings

@lru_cache()
def google_auth_settings():
    return GoogleAuthSettings() # type: ignore

@lru_cache()
def web_settings():
    return WebSettings() # type: ignore

# python -m app.core.config
if __name__ == "__main__":
    settings = postgre_settings()
    print( settings.DATABASE_URL )