import logging

from fastapi import FastAPI
import uvicorn

from src.app.initializer import init
from src.app.config import common_config, openapi_config

logger = logging.getLogger()

app = FastAPI(
    title=openapi_config.name,
    description=openapi_config.description,
    version=openapi_config.version,
    openapi_url=f"{common_config.API_V1_STR}/openapi.json"
)

logger.info("Starting application initialization...")
init(app)
logger.info("Successfully initialized!")

if __name__ == "__main__":
    uvicorn.run(app)
    # uvicorn.run(app, host='0.0.0.0', port=common_config.SERVICE_PORT, log_level=logging.DEBUG)
