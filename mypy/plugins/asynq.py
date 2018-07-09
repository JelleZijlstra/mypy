from mypy.nodes import ARG_POS
from mypy.plugin import FunctionContext
from mypy.types import (
    Type, Instance, CallableType, TypedDictType, UnionType, NoneTyp, TypeVarType,
    AnyType, TypeList, UnboundType, TypeOfAny
)


def asynq_callback(ctx: FunctionContext) -> Type:
    function_type = ctx.api.named_type('builtins.function')
    print(ctx)
    # This approach doesn't work because we don't have access to the function
    # object, so we can't make an _AsyncDecoratorFunction that knows about the
    # real argument types of this function.
    # ???
    # How do we do this?
    # Also, if we go with AsyncDecorator, will it handle @async methods correctly?

    return CallableType(
        arg_types=[AnyType(TypeOfAny.special_form)],
        arg_kinds=[ARG_POS],
        arg_names=[None],
        ret_type=AnyType(TypeOfAny.from_error),
        fallback=function_type,
        implicit=True,
    )
