from src.core.exceptions import ConflictError, InternalServerError, NotFoundError


class LeadError:
    @classmethod
    def not_found(cls, detail: str = "Lead não encontrado"):
        return NotFoundError("Lead", detail)

    @classmethod
    def email_already_exists(cls):
        return ConflictError("Já existe um lead com este email", resource="Lead")

    @classmethod
    def internal_server_error(cls, detail: str = "Erro interno no módulo Lead"):
        return InternalServerError(detail)
