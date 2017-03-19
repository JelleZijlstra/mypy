# builtins stub for asynq
from typing import Any, Iterable, TypeVar

class object: pass
class list: pass
class function: pass
class int: pass
class ellipsis: pass
class tuple: pass
class str: pass
class type: pass
class dict: pass

def range(n: int) -> Iterable[int]: ...

T = TypeVar('T')
def sum(xs: Iterable[T]) -> T: ...
