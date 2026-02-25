from fastapi import APIRouter

from src.core.base import DomainModule
from src.core.module_helper import simple_provider

from .repository import LeadRepository
from .router import router as _router
from .use_cases.lead_use_cases import LeadUseCases


@simple_provider(LeadRepository)
@simple_provider(LeadUseCases)
class LeadModule(DomainModule):
    @property
    def router(self) -> APIRouter:
        return _router
