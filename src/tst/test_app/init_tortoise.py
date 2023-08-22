from tortoise import Tortoise
from src.db import tortoise_config


async def async_init_db() -> None:

    await Tortoise.init(
            db_url=tortoise_config.db_url,
            modules={"models": ["aerich.models",
                                "src.app.models.tortoise.event"]}
        )
    return None