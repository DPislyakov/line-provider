from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" ALTER COLUMN "coefficient" TYPE DECIMAL(22,11) USING "coefficient"::DECIMAL(22,11);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" ALTER COLUMN "coefficient" TYPE DECIMAL(20,10) USING "coefficient"::DECIMAL(20,10);"""
