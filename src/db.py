"""Config of DB"""
from pydantic import Field
from pydantic_settings import BaseSettings


POSTGRES_DB_URL = "postgres://{postgres_user}:{postgres_password}@{postgres_host}:" \
                  "{postgres_port}/{postgres_db}"


class PostgresSettings(BaseSettings):
    """Postgres env values"""
    postgres_db: str = Field("line_provider", env="POSTGRES_DB")
    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    postgres_host: str = Field("localhost", env="POSTGRES_HOST")
    postgres_port: str = Field("5432", env="POSTGRES_PORT")

    class Config:
        case_sensitive = False


class TortoiseSettings(BaseSettings):
    """Tortoise-ORM settings"""

    db_url: str
    generate_schemas: bool

    @classmethod
    def generate(cls):
        """Generate Tortoise-ORM settings"""

        postgres = PostgresSettings()
        db_url = POSTGRES_DB_URL.format(**postgres.dict())
        del postgres

        return TortoiseSettings(db_url=db_url, generate_schemas=True)

    class Config:
        env_file = "./envs/dev.env"
        case_sensitive = False


tortoise_config = TortoiseSettings.generate()

TORTOISE_ORM = {
    "connections": {
        "default": tortoise_config.db_url,
    },
    "apps": {
        "models": {
            "models":[
                "aerich.models",
                "src.app.models.tortoise.event"
            ],
            "connection": "default"
        },
    }
}
