from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingConfig(BaseSettings):
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_datefmt: str = "%Y-%m-%d %H:%M:%S"
    log_file: str = "logs/streamlit/{name}.log"
    log_max_bytes: int = 1024 * 1024
    log_backup_count: int = 3

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ClientAPIConfig(BaseSettings):
    fastapi_host: str = "http://fastapi"
    fastapi_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Config(BaseSettings):
    log_config: LoggingConfig = LoggingConfig()
    client_config: ClientAPIConfig = ClientAPIConfig()


@lru_cache
def get_config():
    return Config()
