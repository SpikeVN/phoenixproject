import abc
import random
from typing import Callable

from . import command, fb
from phoenix.fb import ThreadType
from .globals import COMMAND_REGISTRY
from .hack import get_module


class Module(abc.ABC):
    """
    Represents a bot module.
    """

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot


class Bot(fb.Client):
    # noinspection PyMissingConstructor
    def __init__(self, prefix: str = "!", answer_self: bool = False):
        self.prefix = prefix
        self.answer_self = answer_self
        self.modlist: dict[str, Module] = {}
        self.botcmds: dict[str, Callable[[any, list[str]], bool]] = {}

    def run(self, email: str, password: str, *, use_selenium: bool = False):
        """
        Runs the bot using credentials provided.

        :param email: the email of the Facebook user
        :param password: the password of the Facebook user
        :param use_selenium: whether to use the more robust Selenium-based
            login.
        """
        super().__init__(email, password, use_selenium_for_login=use_selenium)
        super().listen()

    def invoke_command(self, ctx: command.Context, content: str):
        """
        Parse the command and pass it onto the individual handlers.
        """
        if not self.answer_self and ctx.author_id == self.uid:
            return

        if content.startswith(self.prefix):
            cmd, *args = content[1:].split()
            # TODO - command execution error handling
            result = False
            callee = COMMAND_REGISTRY.get(cmd.lower())
            if callee is None:
                callee = self.botcmds.get(cmd.lower())
                if callee is None:
                    ctx.reply(
                        random.choice(
                            [
                                "tf noi ccjv",
                                "bố đéo",
                                "m cút",
                                "tf",
                                "🖕 go fuck yourself",
                                "💩",
                                "🐒💨",
                                "gtfo",
                            ]
                        )
                    )
                    return
                else:
                    if not callee(ctx, args):
                        ctx.reply("chịu. hỏi khó thế ai bt")
            else:
                if not callee(self.modlist[get_module(callee).__name__], ctx, args):
                    ctx.reply("chịu. hỏi khó thế ai bt")

    def register_module(self, m):
        mod = m.get(self)
        if mod is not None:
            self.modlist[type(mod).__name__] = mod

    def add_or_edit_command(
        self, name: str, callback: Callable[[any, list[str]], bool]
    ):
        self.botcmds[name] = callback

    # TODO - Event listener

    def onMessage(
        self,
        mid=None,
        author_id=None,
        message=None,
        message_object=None,
        thread_id=None,
        thread_type=ThreadType.USER,
        ts=None,
        metadata=None,
        msg=None,
    ):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        self.invoke_command(
            command.Context(
                message_id=mid,
                author_id=author_id,
                message=message_object,
                thread_type=thread_type,
                thread_id=thread_id,
                timestamp=ts,
                metadata=metadata,
                _storage=msg,
                bot=self,
            ),
            message_object.text,
        )
