
import asyncio

from async_lru import alru_cache

from a_sync import exceptions
from a_sync._typing import *

class CacheKwargs(TypedDict):
    maxsize: Optional[int]
    ttl: Optional[int]
    typed: bool

@overload
def apply_async_memory_cache(
    coro_fn: Literal[None],
    **kwargs: Unpack[CacheKwargs]
) -> AsyncDecorator[P, T]:...
    
@overload
def apply_async_memory_cache(
    coro_fn: int,
    **kwargs: Unpack[CacheKwargs]
) -> AsyncDecorator[P, T]:...
    
@overload
def apply_async_memory_cache(
    coro_fn: CoroFn[P, T],
    **kwargs: Unpack[CacheKwargs]
) -> CoroFn[P, T]:...

@overload
def apply_async_memory_cache(
    coro_fn: Literal[None],
    **kwargs: Unpack[CacheKwargs]
) -> AsyncDecorator[P, T]:...

def apply_async_memory_cache(
    coro_fn: Optional[Union[CoroFn[P, T], int]] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[int] = None,
    typed: bool = False,
) -> AsyncDecoratorOrCoroFn[P, T]:
    # Parse Inputs
    if isinstance(coro_fn, int):
        assert maxsize is None
        maxsize = coro_fn
        coro_fn = None
    
    # Validate 
    elif coro_fn is None:
        if maxsize is not None and not isinstance(maxsize, int):
            raise TypeError("'lru_cache_maxsize' must be an integer or None.", maxsize)
    elif not asyncio.iscoroutinefunction(coro_fn):
        raise exceptions.FunctionNotAsync(coro_fn)

    cache_decorator = alru_cache(maxsize=maxsize, ttl=ttl, typed=typed)
    decorated = cache_decorator(coro_fn)
    return cache_decorator if coro_fn is None else decorated