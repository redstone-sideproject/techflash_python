from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GCP_LOCATION: str 
    GCP_PROJECT: str 

    class Config:
        env_file = "src/.env"