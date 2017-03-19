from typing import Any, Callable, Generic, TypeVar

_CT = TypeVar('_CT', bound=Callable[..., Any])
_T = TypeVar('_T')
_ReturnT = TypeVar('_ReturnT')

class AsyncTask(Generic[_T]):
    def value(self) -> _T: ...

class _AsyncDecoratorFunction(Generic[_ReturnT]):
    def __call__(self, *args: Any, **kwargs: Any) -> _ReturnT: ...
    def async(self, *args: Any, **kwargs: Any) -> AsyncTask[_ReturnT]: ...

class _AsyncDecoratorBinder:
    def __call__(self, fn: Callable[..., _ReturnT]) -> _AsyncDecoratorFunction[_ReturnT]: ...

def async(*args: Any) -> _AsyncDecoratorBinder: ...
