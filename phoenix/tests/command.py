from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .. import fb, logutils
from ..globals import COMMAND_REGISTRY


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
        logutils.info(
            f"Sent `{fb.Message(text=content, reply_to_id=self.message.uid)}` to threadID `{self.thread_id}` (type {self.thread_type})"
        )

    def reply(self, content: str, *args, **kwargs):
        # noinspection PyArgumentList
        logutils.info(
            f"Sent `{fb.Message(text=content, reply_to_id=self.message.uid)}` to threadID `{self.thread_id}` (type {self.thread_type})"
        )
        # self.bot.send(
        #     ,
        #     self.thread_id,
        #     self.thread_type,
        #     *args,
        #     **kwargs,
        # )


def cmd_def(
    *, name: str = None
) -> Callable[
    [Callable[[Context, list[str]], bool]], Callable[[Context, list[str]], bool]
]:
    def decorator(f: Callable[[Context, list[str]], bool]):
        COMMAND_REGISTRY[name.lower()] = f
        return f

    return decorator
