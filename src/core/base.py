from abc import ABC

from fastapi import APIRouter
from injector import Module


class DomainModule(Module, ABC):
    __slots__ = ()

    @property
    def router(self) -> APIRouter:
        raise NotImplementedError("Domain modules must implement router property")
