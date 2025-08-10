from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    TELEGRAM_BOT_USERNAME: str

    # Amazon SP-API / LWA
    LWA_ID: str
    LWA_SECRET: str
    REFRESH_TOKEN: str

    # AWS credentials (choose one approach)
    # Option A: long-term IAM user + role assumption (recommended)
    IAM_ROLE_ARN: str | None = None
    IAM_USER_ACCESS_KEY_ID: str | None = None
    IAM_USER_SECRET: str | None = None

    # Option B: STS temporary credentials
    STS_ACCESS_KEY_ID: str | None = None
    STS_SECRET_ACCESS_KEY: str | None = None
    STS_SESSION_TOKEN: str | None = None

    # Marketplace / region
    MARKETPLACE_ID: str
    REGION: str | None = None  # e.g. "na", "eu", "fe" (optional)

    # Optional: override hosts if you really need to (not required for the library)
    HOST: str | None = None
    STS_HOST: str | None = None

    # Polling window in minutes
    POLL_WINDOW_MINUTES: int
    LIST_PRICE: float

    class Config:
        env_file = ".env"

settings = Settings()