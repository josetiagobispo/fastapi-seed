from typing import Type

from .base import DomainModule


class ModuleRegistry:
    _modules: list[Type[DomainModule]] = []
    _module_set: set[Type[DomainModule]] = set()

    @classmethod
    def get_modules(cls) -> list[Type[DomainModule]]:
        return cls._modules

    @classmethod
    def register_module(cls, module: Type[DomainModule]) -> None:
        if module not in cls._module_set:
            cls._modules.append(module)
            cls._module_set.add(module)

    @classmethod
    def register_modules(cls, modules: list[Type[DomainModule]]) -> None:
        for module in modules:
            cls.register_module(module)

    @classmethod
    def clear_modules(cls) -> None:
        cls._modules.clear()
        cls._module_set.clear()
