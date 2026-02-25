from typing import Type, TypeVar

T = TypeVar("T")


def auto_inject(cls: Type[T]) -> Type[T]:
    setattr(cls, "_auto_injectable", True)
    return cls


def repository(cls: Type[T]) -> Type[T]:
    setattr(cls, "_is_repository", True)
    return auto_inject(cls)


def use_case(cls: Type[T]) -> Type[T]:
    setattr(cls, "_is_use_case", True)
    return auto_inject(cls)


def service(cls: Type[T]) -> Type[T]:
    setattr(cls, "_is_service", True)
    return auto_inject(cls)
