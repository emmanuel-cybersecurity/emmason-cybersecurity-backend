from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
app_name: str = "Emmason Cyber Security API"
environment: str = "development"
database_url: str = "sqlite:///./emmason.db"

jwt_secret: str = "CHANGE_THIS_IN_PRODUCTION"
jwt_algorithm: str = "HS256"
access_token_minutes: int = 30

admin_username: str = "admin"
admin_password: str = "CHANGE_THIS_IN_PRODUCTION"

cors_origins_raw: str = "http://localhost:3000,http://localhost:5173"

model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
)

@property
def cors_origins(self) -> list[str]:
    return [
        x.strip()
        for x in self.cors_origins_raw.split(",")
        if x.strip()
    ]

@lru_cache
def get_settings() -> Settings:
return Settings()

settings = get_settings()
