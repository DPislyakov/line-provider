from pydantic_settings import BaseSettings
from . import common_config

OPENAPI_API_DESCRIPTION = "API for LIMBeauty service"


class OpenAPISettings(BaseSettings):
    name: str
    version: str
    description: str

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=common_config.PROJECT_NAME,
            version=common_config.SERVICE_VERSION,
            description=OPENAPI_API_DESCRIPTION,
        )


openapi_config = OpenAPISettings.generate()
