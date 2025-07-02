from typing import Callable

import httpx
import pytest

from src import app


@pytest.fixture
async def client():
    """Возвращает клиент для работы с HTTP API приложения."""

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
