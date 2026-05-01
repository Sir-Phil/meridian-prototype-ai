from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    # This default is fine, but .env overrides it
    MCP_SERVER_URL: str = "https://order-mcp-74afyau24q-uc.a.run.app/mcp"
    MODEL_NAME: str = "openai/gpt-4o-mini" 
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    ENV_MODE: str = "development"
    PORT: int = 7860

    # ADD THIS VALIDATOR TO STRIP BRACKETS/QUOTES
    @field_validator("MCP_SERVER_URL", mode="before")
    @classmethod
    def clean_mcp_url(cls, v: str) -> str:
        if isinstance(v, str):
            # Removes spaces, brackets, and quotes
            return v.strip().strip("[]").strip("'").strip('"')
        return v

    # model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    model_config = SettingsConfigDict(
    env_file=".env", 
    env_file_encoding='utf-8', 
    extra="ignore",
    env_ignore_empty=True # Useful for Vercel
)

settings = Settings()