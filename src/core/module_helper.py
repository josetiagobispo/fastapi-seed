import inspect
from typing import Type, TypeVar

from injector import provider, singleton

T = TypeVar("T")


def simple_provider(dependency_class: Type[T]):
    def decorator(module_class):
        provider_name = f"provide_{dependency_class.__name__.lower()}"
        sig = inspect.signature(dependency_class.__init__)

        def provider_method(self, **kwargs):
            return dependency_class(**kwargs)

        annotations = {}
        for param_name, param in sig.parameters.items():
            if param_name != "self" and param.annotation != inspect.Parameter.empty:
                annotations[param_name] = param.annotation

        annotations["return"] = dependency_class
        provider_method.__annotations__ = annotations
        provider_method.__name__ = provider_name
        provider_method.__qualname__ = f"{module_class.__name__}.{provider_name}"

        decorated = singleton(provider(provider_method))
        setattr(module_class, provider_name, decorated)

        return module_class

    return decorator
