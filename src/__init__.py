from pydantic import BaseModel

_BASE_CONFIG = {"from_attributes": True}
_RESPONSE_CONFIG = {
    "from_attributes": True,
    "populate_by_name": True,
    "arbitrary_types_allowed": True,
}


class BaseDTO(BaseModel):
    model_config = _BASE_CONFIG


class BaseDTOResponse(BaseDTO):
    model_config = _RESPONSE_CONFIG
