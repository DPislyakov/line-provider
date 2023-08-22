import os
import logging
import uuid

import fastapi
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.starlette import register_tortoise

from src.app.api import api_v1_router
from src.app.config import common_config
from src.app.config.db import TORTOISE_ORM as TORTOISE_ORM_CONFIG

logger = logging.getLogger(__name__)


def init(app: FastAPI):
    """
    Init all app parts
    """
    init_routers(app)
    init_middlewares(app)
    if common_config.BACKEND_CORS_ORIGINS:
        init_cors(app)
    init_db(app)


def init_db(app: FastAPI):
    """
    Init database models.
    """
    logger.info("Starting db initialization...")
    register_tortoise(
        app,
        config=TORTOISE_ORM_CONFIG
    )
    logger.info("Successfully db initialized")


def init_routers(app: FastAPI):
    """
    Initialize routers defined in `app.api`
    """
    app.include_router(api_v1_router, prefix=common_config.API_V1_STR)
    print("1")


def init_middlewares(app: FastAPI):
    """
    Initialize middlewares
    """

    middle_logger = logging.getLogger("MIDDLE")

    @app.middleware("http")
    async def log_it(request: Request, call_next) -> fastapi.Response:
        """
        Log request and response
        """

        random_req_id = str(uuid.uuid4())[:8]

        req_data = [
            random_req_id,
            f"{request.client[0]}:{request.client[1]} >>>",
            request.method,
            f"{request.url}",
        ]
        middle_logger.info(" > ".join(req_data))
        response = await call_next(request)

        res_body = b''
        async for chunk in response.body_iterator:
            res_body += chunk

        resp_data = [
            random_req_id,
            f"{request.client[0]}:{request.client[1]} <<<",
            f"{response.status_code}",
            f"({len(res_body)})",
        ]
        middle_logger.info(" < ".join(resp_data))
        middle_logger.debug(" < ".join([random_req_id, "DATA", str(res_body)]))

        return fastapi.Response(content=res_body, status_code=response.status_code,
                                headers=dict(response.headers), media_type=response.media_type)


def init_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in common_config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

