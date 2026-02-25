import pytest
from pydantic import ValidationError

from modules.lead.schemas.base import LeadCreate, LeadResponse


def test_lead_create_valido():
    lead = LeadCreate(name="Maria", email="maria@test.com", phone="11999990000")
    assert lead.name == "Maria"
    assert lead.email == "maria@test.com"
    assert lead.phone == "11999990000"


def test_lead_create_telefone_com_formatacao():
    lead = LeadCreate(name="Maria", email="maria@test.com", phone="+55 (11) 99999-0000")
    assert lead.phone == "5511999990000"


def test_lead_create_nome_curto():
    with pytest.raises(ValidationError):
        LeadCreate(name="A", email="a@b.com", phone="11999990000")


def test_lead_create_nome_com_numeros():
    with pytest.raises(ValidationError):
        LeadCreate(name="Maria123", email="a@b.com", phone="11999990000")


def test_lead_create_email_invalido():
    with pytest.raises(ValidationError):
        LeadCreate(name="Maria", email="nao-e-email", phone="11999990000")


def test_lead_create_telefone_curto():
    with pytest.raises(ValidationError):
        LeadCreate(name="Maria", email="a@b.com", phone="123")


def test_lead_create_telefone_com_letras():
    with pytest.raises(ValidationError):
        LeadCreate(name="Maria", email="a@b.com", phone="1199abc0000")


def test_lead_create_campos_obrigatorios():
    with pytest.raises(ValidationError):
        LeadCreate()


def test_lead_response_com_birth_date():
    resp = LeadResponse(
        id="abc", name="Test", email="t@t.com", phone="11999990000", birth_date="1996-5-30"
    )
    assert resp.birth_date == "1996-5-30"


def test_lead_response_sem_birth_date():
    resp = LeadResponse(id="abc", name="Test", email="t@t.com", phone="11999990000")
    assert resp.birth_date is None
