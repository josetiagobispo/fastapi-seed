from fastapi import APIRouter, Depends, status

from src.core.dependencies import inject_dependency

from .schemas.base import LeadCreate, LeadResponse
from .use_cases.lead_use_cases import LeadUseCases

router = APIRouter(
    prefix="/api/v1/leads",
    tags=["leads"],
)


@router.post(
    "/",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar Lead",
    description="Cria um novo lead com enriquecimento automático de birth_date via API externa",
)
async def create_lead(
    data: LeadCreate,
    use_cases: LeadUseCases = Depends(inject_dependency(LeadUseCases)),
) -> LeadResponse:
    return await use_cases.create_lead(data)


@router.get(
    "/",
    response_model=list[LeadResponse],
    summary="Listar Leads",
    description="Lista todos os leads cadastrados",
)
async def list_leads(
    use_cases: LeadUseCases = Depends(inject_dependency(LeadUseCases)),
) -> list[LeadResponse]:
    return await use_cases.list_leads()


@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
    summary="Buscar Lead",
    description="Retorna os detalhes de um lead específico pelo ID",
)
async def get_lead(
    lead_id: str,
    use_cases: LeadUseCases = Depends(inject_dependency(LeadUseCases)),
) -> LeadResponse:
    return await use_cases.get_lead(lead_id)
