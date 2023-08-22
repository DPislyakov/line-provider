import os
from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    PROJECT_NAME: str = "Line Provider API"
    SECRET_KEY: str = 'w1-eyubinlxauy+wrtp)vug@bmja=g-iw+a3b(!s^i_nvnmf!*'
    SERVICE_NAME: str = "line_provider"

    API_V1_STR: str = "/v1/app"
    SERVICE_VERSION: str = "0.0.1"
    SERVICE_PORT: int = 8000

    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    ALLOW_EXTERNAL_SIGNUP: bool = True

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    EVENT_UPDATE_TIMEOUT: int = 8

    EVENT_ACTIVE_HM: str = "active_events"
    EVENT_FINISHED_HM: str = "finished_events"

    class Config:
        env_file = os.getenv("ENV_FILE", default="../envs/local.env")
        case_sensitive = False


common_config = CommonSettings()
