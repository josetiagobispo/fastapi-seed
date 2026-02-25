from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.database.interfaces.mongodb_port import MongoDBPort


class MongoDBAdapter(MongoDBPort):
    def __init__(self, connection_string: str, database_name: str):
        super().__init__(connection_string, database_name)

    @property
    def _collection(self) -> AsyncIOMotorCollection:
        if not self._table_name:
            raise ValueError("Table name not set. Call set_table first.")
        return self._database[self._table_name]

    async def create(self, data: dict) -> dict:
        result = await self._collection.insert_one(data)
        created_doc = await self._collection.find_one({"_id": result.inserted_id})
        return self._serialize_doc(created_doc)

    async def read(self, identifier: Any) -> dict | None:
        if isinstance(identifier, str) and ObjectId.is_valid(identifier):
            identifier = ObjectId(identifier)
        doc = await self._collection.find_one({"_id": identifier})
        return self._serialize_doc(doc) if doc else None

    async def update(self, identifier: Any, data: dict) -> bool:
        if isinstance(identifier, str) and ObjectId.is_valid(identifier):
            identifier = ObjectId(identifier)
        result = await self._collection.update_one({"_id": identifier}, {"$set": data})
        return result.modified_count > 0

    async def delete(self, identifier: Any) -> bool:
        if isinstance(identifier, str) and ObjectId.is_valid(identifier):
            identifier = ObjectId(identifier)
        result = await self._collection.delete_one({"_id": identifier})
        return result.deleted_count > 0

    async def find(self, query: dict) -> list[dict]:
        cursor = self._collection.find(query)
        return [self._serialize_doc(doc) async for doc in cursor]

    @staticmethod
    def _serialize_doc(doc: dict | None) -> dict | None:
        if doc is None:
            return None
        doc["id"] = str(doc.pop("_id"))
        return doc
