from typing import Type, TypeVar, Callable, overload

from .context import Auto, Context


A = TypeVar("A", bound=Context)
B = TypeVar("B")

@overload
def auto(
    context_type: Type[A] = None,
    context_name: str = None
) -> A:
    ...

@overload
def auto(
    context_type: Type[A],
    context_name: str = None,
    instance_type: type[B] = None,
) -> B:
    ...

@overload
def auto(
    context_type: Type[A],
    context_name: str = None,
    instance_factory: Callable[[str], B] = None
) -> B:
    ...

def auto(
    context_name = None,
    instance_type = None, 
    instance_factory = None
) -> Auto:
    return Auto(
        context_name,
        instance_type,
        instance_factory
    )
