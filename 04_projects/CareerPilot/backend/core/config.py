from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Core
    database_url: str = Field(..., alias="DATABASE_URL")
    secret_key: str = Field(..., alias="SECRET_KEY")
    environment: str = Field("development", alias="ENVIRONMENT")

    # Groq
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")

    # Telegram
    telegram_bot_token: str = Field("", alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str = Field("", alias="TELEGRAM_CHAT_ID")

    # Gmail
    google_client_id: str = Field("", alias="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field("", alias="GOOGLE_CLIENT_SECRET")
    google_pubsub_topic: str = Field("", alias="GOOGLE_PUBSUB_TOPIC")

    # LinkedIn
    linkedin_email: str = Field("", alias="LINKEDIN_EMAIL")
    linkedin_password: str = Field("", alias="LINKEDIN_PASSWORD")

    # Naukri
    naukri_email: str = Field("", alias="NAUKRI_EMAIL")
    naukri_password: str = Field("", alias="NAUKRI_PASSWORD")

    # Indeed
    indeed_email: str = Field("", alias="INDEED_EMAIL")
    indeed_password: str = Field("", alias="INDEED_PASSWORD")

    class Config:
        env_file = ".env"
        populate_by_name = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_yaml_config() -> dict:
    config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


_yaml_config: Optional[dict] = None


def get_yaml_config() -> dict:
    global _yaml_config
    if _yaml_config is None:
        _yaml_config = load_yaml_config()
    return _yaml_config
