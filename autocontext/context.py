from __future__ import annotations

import os
from typing import TypeVar, Callable, Generic
from inspect import get_annotations


C = TypeVar("C")
T = TypeVar("T")


class Context(Generic[C]):

    instances: dict[str, C] = None

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def env(self, key):
        key = f"{self.context_name}_{key}" if self.context_name else key
        return os.getenv(key)

    def __init__(self, context_name: str) -> None:
        super().__init__()
        self.context_name = context_name
        cls = self.__class__
        for key, annotation in get_annotations(cls).items():
            value = getattr(cls, key)
            if isinstance(value, Auto):
                value.get_instance(
                    annotation, self.context_name)

    @classmethod
    def factory(cls, context_name: str) -> C:
        return cls(context_name)

    @classmethod
    def instance(cls, context_name: str = None) -> C:
        if cls.instances is None:
            cls.instances = {}
        return cls.instances.setdefault(
            context_name, cls.factory(context_name))


A = TypeVar("A", bound=Context)
D = TypeVar("D")


class Auto(Generic[A, D]):

    def __init__(
        self,
        context_type: A = None,
        context_name: str = None,
        instance_type: type[D] = type[A],
        instance_factory: Callable[[str], D] = None
    ) -> None:
        self.context_type = context_type
        self.context_name = context_name
        self.instance_type = instance_type
        self.instance_factory = instance_factory

    def get_instance(self, context_type, parent_context_name: str) -> D:
        context_name = self.context_name or parent_context_name
        context_type = self.context_type or context_type

        if self.instance_factory:
            return self.instance_factory(context_name)

        return context_type.instance(context_name)
