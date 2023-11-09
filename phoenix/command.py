from __future__ import annotations
from typing import Callable, List
from dataclasses import dataclass


from . import fb
from .globals import COMMAND_REGISTRY


@dataclass
class Context:
    message_id: str
    author_id: str
    message: fb.Message
    thread_type: fb.Thread
    thread_id: int
    timestamp: int
    metadata: any
    _storage: any
    bot: fb.Client

    def send_message(self, content: str, *args, **kwargs):
        # noinspection PyArgumentList
        self.bot.send(
            content,
            self.thread_id,
            self.thread_type,
            *args,
            **kwargs,
        )

    def reply(self, content: str, *args, **kwargs):
        # noinspection PyArgumentList
        self.bot.send(
            fb.Message(text=content, reply_to_id=self.message.uid),
            self.thread_id,
            self.thread_type,
            *args,
            **kwargs,
        )


def cmd_def(
    *, name: str = None
) -> Callable[
    [Callable[[Context, list[str]], bool]], Callable[[Context, list[str]], bool]
]:
    def decorator(f: Callable[[Context, list[str]], bool]):
        COMMAND_REGISTRY[name.lower()] = f
        return f

    return decorator
