from datetime import datetime

from pydantic import BaseModel, Field


class LeadModel(BaseModel):
    name: str = Field(..., description="Nome do lead")
    email: str = Field(..., description="Email do lead")
    phone: str = Field(..., description="Telefone do lead")
    birth_date: str | None = Field(default=None, description="Data de nascimento")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
