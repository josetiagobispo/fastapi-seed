from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from .database_port import DatabasePort


class MongoDBPort(DatabasePort):
    def __init__(self, connection_string: str, database_name: str):
        self._client = AsyncIOMotorClient(connection_string)
        self._database = self._client[database_name]
        self._table_name: str | None = None
        self._model = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if not self._table_name:
            raise ValueError("Table name not set. Call set_table first.")
        return self._database[self._table_name]

    async def create(self, data: dict) -> Any: ...

    async def read(self, identifier: Any) -> Any | None: ...

    async def update(self, identifier: Any, data: dict) -> bool:
        result = await self.collection.update_one({"_id": identifier}, {"$set": data})
        return result.modified_count > 0

    async def delete(self, identifier: Any) -> bool:
        result = await self.collection.delete_one({"_id": identifier})
        return result.deleted_count > 0

    async def find(self, query: dict) -> list[Any]: ...
