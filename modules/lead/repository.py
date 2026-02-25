from src.core.decorators import repository
from src.database.interfaces.mongodb_port import MongoDBPort

from .const import COLLECTION_NAME
from .schemas.base import LeadResponse


@repository
class LeadRepository:
    def __init__(self, database: MongoDBPort):
        self._database = database
        self._database.set_table(COLLECTION_NAME)

    async def create(self, data: dict) -> LeadResponse:
        result = await self._database.create(data)
        return LeadResponse.model_validate(result)

    async def find_all(self) -> list[LeadResponse]:
        results = await self._database.find({})
        return [LeadResponse.model_validate(doc) for doc in results]

    async def find_by_id(self, lead_id: str) -> LeadResponse | None:
        result = await self._database.read(lead_id)
        if not result:
            return None
        return LeadResponse.model_validate(result)

    async def find_by_email(self, email: str) -> LeadResponse | None:
        results = await self._database.find({"email": email})
        if not results:
            return None
        return LeadResponse.model_validate(results[0])

    async def update_birth_date(self, lead_id: str, birth_date: str) -> None:
        await self._database.update(lead_id, {"birth_date": birth_date})
