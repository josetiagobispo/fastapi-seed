"""
Migration 001 - Criar collection leads com índices

MongoDB não exige migrations como bancos relacionais,
mas é boa prática versionar a criação de índices e validações.

Uso:
    python -m migrations.001_create_leads_collection
"""

import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from settings import Settings


async def upgrade() -> None:
    settings = Settings()
    client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING)
    db = client[settings.MONGODB_DB_NAME]

    if "leads" not in await db.list_collection_names():
        await db.create_collection("leads")

    leads = db["leads"]
    await leads.create_index("email", unique=False)
    await leads.create_index("phone", unique=False)
    await leads.create_index("created_at")

    print("Collection 'leads' criada com índices")
    client.close()


async def downgrade() -> None:
    settings = Settings()
    client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING)
    db = client[settings.MONGODB_DB_NAME]

    await db.drop_collection("leads")

    print("Collection 'leads' removida")
    client.close()


if __name__ == "__main__":
    asyncio.run(upgrade())
