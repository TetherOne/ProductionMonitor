from pydantic import BaseModel, PostgresDsn
from pydantic_settings import SettingsConfigDict, BaseSettings


class APIPrefix(BaseModel):
    prefix: str = "/api"
    shift_tasks: str = "/shift-tasks"
    product_codes: str = "/product-codes"

    @property
    def full_prefix(self) -> str:
        return f"{self.prefix}"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 40
    max_overflow: int = 8


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="envs/app.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="PRODUCTION_MONITOR__",
        arbitrary_types_allowed=True,
    )
    api: APIPrefix = APIPrefix()
    db: DatabaseConfig


settings = Settings()
