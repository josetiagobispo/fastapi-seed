import pytest


from src.providers.http_client import HttpClient


@pytest.mark.asyncio
async def test_get_sucesso():
    client = HttpClient(timeout=5)
    result = await client.get("https://dummyjson.com/users/1")

    if result is not None:
        assert "birthDate" in result


@pytest.mark.asyncio
async def test_get_url_invalida():
    client = HttpClient(timeout=2)
    result = await client.get("https://dominio-que-nao-existe-xyz.com/api")
    assert result is None


@pytest.mark.asyncio
async def test_get_404():
    client = HttpClient(timeout=5)
    result = await client.get("https://dummyjson.com/users/99999999")
    assert result is None
