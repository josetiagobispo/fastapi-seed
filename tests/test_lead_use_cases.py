import asyncio

import pytest
from unittest.mock import AsyncMock

from modules.lead.schemas.base import LeadCreate, LeadResponse
from modules.lead.use_cases.lead_use_cases import LeadUseCases
from src.providers.dummy_json_client import DummyJsonClient


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_dummy_json():
    return AsyncMock(spec=DummyJsonClient)


@pytest.fixture
def use_cases(mock_repository, mock_dummy_json):
    return LeadUseCases(repository=mock_repository, dummy_json=mock_dummy_json)


@pytest.fixture
def lead_data():
    return LeadCreate(name="João Silva", email="joao@email.com", phone="11999998888")


@pytest.fixture
def lead_response():
    return LeadResponse(
        id="abc123",
        name="João Silva",
        email="joao@email.com",
        phone="11999998888",
        birth_date="1996-5-30",
    )


@pytest.mark.asyncio
async def test_create_lead_com_birth_date(use_cases, mock_repository, mock_dummy_json, lead_data, lead_response):
    mock_dummy_json.fetch_birth_date.return_value = "1996-5-30"
    mock_repository.create.return_value = lead_response

    result = await use_cases.create_lead(lead_data)
    await asyncio.sleep(0.1)

    assert result.id == "abc123"
    mock_repository.create.assert_called_once()
    call_args = mock_repository.create.call_args[0][0]
    assert call_args["birth_date"] is None
    mock_repository.update_birth_date.assert_called_once_with("abc123", "1996-5-30")


@pytest.mark.asyncio
async def test_create_lead_api_externa_falha(use_cases, mock_repository, mock_dummy_json, lead_data):
    mock_dummy_json.fetch_birth_date.return_value = None
    mock_repository.create.return_value = LeadResponse(
        id="abc123", name="João Silva", email="joao@email.com", phone="11999998888", birth_date=None,
    )

    result = await use_cases.create_lead(lead_data)
    await asyncio.sleep(0.1)

    assert result.birth_date is None
    call_args = mock_repository.create.call_args[0][0]
    assert call_args["birth_date"] is None
    mock_repository.update_birth_date.assert_not_called()


@pytest.mark.asyncio
async def test_list_leads(use_cases, mock_repository, lead_response):
    mock_repository.find_all.return_value = [lead_response]

    result = await use_cases.list_leads()

    assert len(result) == 1
    assert result[0].name == "João Silva"


@pytest.mark.asyncio
async def test_list_leads_vazio(use_cases, mock_repository):
    mock_repository.find_all.return_value = []

    result = await use_cases.list_leads()

    assert result == []


@pytest.mark.asyncio
async def test_get_lead_encontrado(use_cases, mock_repository, lead_response):
    mock_repository.find_by_id.return_value = lead_response

    result = await use_cases.get_lead("abc123")

    assert result.id == "abc123"
    assert result.email == "joao@email.com"


@pytest.mark.asyncio
async def test_get_lead_nao_encontrado(use_cases, mock_repository):
    mock_repository.find_by_id.return_value = None

    with pytest.raises(Exception) as exc_info:
        await use_cases.get_lead("id_invalido")

    assert exc_info.value.status_code == 404
