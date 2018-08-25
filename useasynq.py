from asynq import async

reveal_type(async())

@async()
def f() -> int:
    return 3

reveal_type(f)
