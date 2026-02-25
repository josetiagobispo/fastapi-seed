from typing import Any

from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        custom_field: str | None = None,
        extra_data: dict[str, Any] | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.custom_field = custom_field
        self.extra_data = extra_data or {}


class ValidationError(BaseAppException):
    def __init__(self, detail: str = "Dados inválidos", field: str | None = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            custom_field=field,
        )


class NotFoundError(BaseAppException):
    def __init__(self, resource: str = "Recurso", detail: str | None = None):
        message = detail or f"{resource} não encontrado"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
            custom_field=resource,
        )


class ConflictError(BaseAppException):
    def __init__(self, detail: str = "Conflito detectado", resource: str | None = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            custom_field=resource,
        )


class InternalServerError(BaseAppException):
    def __init__(self, detail: str = "Erro interno do servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
