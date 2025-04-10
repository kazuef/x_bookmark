from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DifyApiKeySettings(BaseSettings):
    model_config = SettingsConfigDict(
        # env_prefix='DIFY_API_KEY_',
        env_file="env/.env",
        env_file_encoding="utf-8",
    )

    csv_to_json: str | None = Field(default=None, alias="DIFY_API_KEY_CSV_TO_JSON")
    categorize_json: str | None = Field(default=None, alias="DIFY_API_KEY_CATEGORIZE_JSON")

