import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class LeadCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Nome do lead",
    )
    email: EmailStr = Field(
        ...,
        description="Email do lead",
    )
    phone: str = Field(
        ...,
        min_length=8,
        max_length=20,
        description="Telefone do lead",
        examples=["11999998888"],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not re.match(r"^[a-zA-ZÀ-ÿ\s]+$", v.strip()):
            raise ValueError("Nome deve conter apenas letras")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-\(\)\+]", "", v)
        if not cleaned.isdigit():
            raise ValueError("Telefone deve conter apenas números")
        if len(cleaned) < 8 or len(cleaned) > 15:
            raise ValueError("Telefone deve ter entre 8 e 15 dígitos")
        return cleaned


class LeadResponse(BaseModel):
    id: str = Field(description="Identificador único do lead")
    name: str = Field(description="Nome do lead")
    email: str = Field(description="Email do lead")
    phone: str = Field(description="Telefone do lead")
    birth_date: str | None = Field(default=None, description="Data de nascimento")

    model_config = {"from_attributes": True}
