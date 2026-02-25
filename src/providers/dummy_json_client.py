from loguru import logger

from src.providers.http_client import HttpClient


class DummyJsonClient:
    def __init__(self, http_client: HttpClient, base_url: str):
        self._http = http_client
        self._base_url = base_url

    async def fetch_birth_date(self) -> str | None:
        response = await self._http.get(self._base_url)
        if response and "birthDate" in response:
            return response["birthDate"]
        logger.warning("Falha ao obter birth_date da API externa, retornando null")
        return None
