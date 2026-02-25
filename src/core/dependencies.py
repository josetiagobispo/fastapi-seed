from typing import Callable, Type, TypeVar

from fastapi import Request
from injector import Injector

T = TypeVar("T")

_dependency_cache: dict[type, Callable] = {}
_global_injector: Injector | None = None


def setup_injector() -> Injector:
    global _global_injector
    if _global_injector is None:
        from src.core.container import AppContainer
        from src.core.registry import ModuleRegistry

        core_modules = [AppContainer()]
        domain_modules = [module() for module in ModuleRegistry.get_modules()]
        _global_injector = Injector(core_modules + domain_modules)
    return _global_injector


def get_injector() -> Injector:
    global _global_injector
    if _global_injector is None:
        return setup_injector()
    return _global_injector


def inject_dependency(dependency_class: Type[T]) -> Callable[[Request], T]:
    if dependency_class not in _dependency_cache:
        def _get_dependency(request: Request) -> T:
            instance = request.app.state.injector.get(dependency_class)
            return instance

        _dependency_cache[dependency_class] = _get_dependency

    return _dependency_cache[dependency_class]
