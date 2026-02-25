from abc import ABC, abstractmethod
from typing import Any


class DatabasePort(ABC):
    _table_name: str | None = None
    _model: Any = None

    def set_table(self, table_name: str) -> None:
        self._table_name = table_name

    def set_model(self, model: Any) -> None:
        self._model = model

    @abstractmethod
    async def create(self, data: dict) -> Any: ...

    @abstractmethod
    async def read(self, identifier: Any) -> Any | None: ...

    @abstractmethod
    async def update(self, identifier: Any, data: dict) -> bool: ...

    @abstractmethod
    async def delete(self, identifier: Any) -> bool: ...

    @abstractmethod
    async def find(self, query: dict) -> list[Any]: ...
