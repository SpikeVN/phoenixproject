from typing import Callable


COMMAND_REGISTRY: dict[str, Callable[[any, any, list[str]], bool]] = {}
