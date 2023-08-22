from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "event" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "coefficient" DECIMAL(20,10),
    "deadline" INT,
    "state" SMALLINT NOT NULL
);
COMMENT ON COLUMN "event"."state" IS 'NEW: 1\nFINISHED_WIN: 2\nFINISHED_LOSE: 3';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
