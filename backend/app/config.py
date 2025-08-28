from pydantic import BaseModel
import os

class Settings(BaseModel):
  env: str = os.getenv("ENV", "dev")
  openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
  model_path: str = os.getenv("MODEL_PATH", "/models/model.joblib")
  allow_origins: str = os.getenv("ALLOW_ORIGINS", "*")


settings = Settings()
