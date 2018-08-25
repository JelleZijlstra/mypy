from typing import Callable

class AsynqFn:
    pass


def _async_impl(fn):
    return AsynqFn()

def async() -> Callable[[object], AsynqFn]:
    return _async_impl

@async()
def x() -> None:
    pass
