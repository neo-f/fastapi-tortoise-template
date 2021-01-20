import ssl
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, FilePath, root_validator
from tortoise import generate_config


class Settings(BaseSettings):
    env: str = "local"
    sentry_dsn: Optional[AnyHttpUrl] = None

    postgres_dsn: PostgresDsn = "postgres://demo:demo@localhost:15432/demo"
    postgres_ssl: bool = False
    postgres_ca_path: Optional[FilePath]
    postgres_key_path: Optional[FilePath]
    postgres_cert_path: Optional[FilePath]

    # pagination
    default_limit: int = 10
    max_limit: int = 1000

    @root_validator
    def check_ssl(cls, values):
        if values.get("postgres_ssl"):
            ca, key, cert = (
                values.get("postgres_ca_path"),
                values.get("postgres_key_path"),
                values.get("postgres_cert_path"),
            )
            if not all((ca, key, cert)):
                raise ValueError("must specify both ca_path,cert_path,key_path while set ssl=True")
        return values

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

db_config = generate_config(
    db_url=settings.postgres_dsn,
    app_modules={"models": ["app.models", "aerich.models"]},
)
if settings.postgres_ssl:
    ssl_ctx = ssl.create_default_context(cafile=str(settings.postgres_ca_path))
    ssl_ctx.load_cert_chain(certfile=settings.postgres_cert_path, keyfile=settings.postgres_key_path)
    ssl_ctx.check_hostname = False
    db_config["connections"]["default"]["credentials"]["ssl"] = ssl_ctx
