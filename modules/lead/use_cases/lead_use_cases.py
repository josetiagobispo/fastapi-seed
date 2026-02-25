import asyncio

from loguru import logger

from src.core.decorators import use_case
from src.providers.dummy_json_client import DummyJsonClient

from ..errors import LeadError
from ..repository import LeadRepository
from ..schemas.base import LeadCreate, LeadResponse


@use_case
class LeadUseCases:
    def __init__(self, repository: LeadRepository, dummy_json: DummyJsonClient):
        self._repository = repository
        self._dummy_json = dummy_json

    async def create_lead(self, data: LeadCreate) -> LeadResponse:
        existing = await self._repository.find_by_email(data.email)
        if existing:
            raise LeadError.email_already_exists()

        lead_data = data.model_dump()
        lead_data["birth_date"] = None
        lead = await self._repository.create(lead_data)

        asyncio.create_task(self._enrich_birth_date(lead.id))

        return lead

    async def list_leads(self) -> list[LeadResponse]:
        return await self._repository.find_all()

    async def get_lead(self, lead_id: str) -> LeadResponse:
        lead = await self._repository.find_by_id(lead_id)
        if not lead:
            raise LeadError.not_found()
        return lead

    async def _enrich_birth_date(self, lead_id: str) -> None:
        birth_date = await self._dummy_json.fetch_birth_date()
        if birth_date:
            await self._repository.update_birth_date(lead_id, birth_date)
            logger.info(f"birth_date atualizado para lead {lead_id}")
