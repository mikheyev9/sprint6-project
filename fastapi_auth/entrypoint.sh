#!/usr/bin/env bash
set -e

echo "Waiting for PostgreSQL to be ready..."
python << END
import time
import asyncpg
import asyncio

async def wait_for_db():
    while True:
        try:
            conn = await asyncpg.connect("postgresql://postgres:qwerty1234@theatre-db:5432/project_collection")
            await conn.close()
            break
        except:
            print("PostgreSQL is not ready yet. Sleeping...")
            time.sleep(2)

asyncio.run(wait_for_db())
print("PostgreSQL is up!")
END

echo "PostgreSQL is up and running!"

echo "Running Alembic migrations..."

alembic upgrade head

exec uvicorn src.main:app --reload --host $UVICORN_HOST --port $UVICORN_PORT_AUTH
