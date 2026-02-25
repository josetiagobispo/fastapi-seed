import asyncio

import httpx
from loguru import logger


class HttpClient:
    def __init__(self, timeout: int = 30, retries: int = 3):
        self._timeout = timeout
        self._retries = retries

    async def get(self, url: str) -> dict | None:
        for attempt in range(1, self._retries + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=httpx.Timeout(self._timeout, connect=self._timeout),
                ) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP {e.response.status_code} ao acessar {url}")
                return None
            except Exception as e:
                logger.warning(
                    f"[{attempt}/{self._retries}] Falha ao acessar {url}: "
                    f"{type(e).__name__}"
                )
                if attempt < self._retries:
                    await asyncio.sleep(1)

        logger.error(f"Todas as {self._retries} tentativas falharam para {url}")
        return None
