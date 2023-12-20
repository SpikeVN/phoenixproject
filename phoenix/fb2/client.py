import enum
from typing import Union

from .errors import PhoenixError
from .. import logutils, events
import aiohttp
import uvloop
import asyncio
from .thread import Thread, ThreadType


class LoginMethod(enum.Enum):
    WEBDRIVER = 1
    REST = 2
    SESSION = 3


class Client:
    """
    A client for the Facebook Chat (Messenger).

    This class contains all the methods you will use to
    interact with Facebook. You can extend this class, and overwrite the ``on`` methods,
    to provide custom event handling (mainly useful while listening).
    """

    listening = False
    """Whether the client is listening.

    Used when creating an external event loop to determine when to stop listening.
    """

    def __init__(
        self,
        email: str,
        password: str,
        user_agent: Union[str, None] = None,
        max_tries: int = 5,
        login_method: LoginMethod = LoginMethod.REST,
        session: aiohttp.Session = None,
        logging_level: int = logutils.INFO,
    ):
        """Logs into Facebook.

        :param email: Facebook ``email``, ``id`` or ``phone number``
        :param password: Facebook account password
        :param user_agent: Custom user agent to use when sending requests. If `None`, user agent will be chosen from a premade list
        :param max_tries: Maximum number of times to try logging in
        :param logging_level: Configures the logging level. Defaults to ``phoenix.logutils.INFO``
        :param login_method: The method used to log in to Facebook.
        """
        self.uid: int = 0
        self.default_thread_id = None
        self.default_thread_type = None
        self.mark_alive = True
        self.buddy_list = {}
        self.mqtt = None
        self.state = None

        logutils.set_min_level(logging_level)
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)
        asyncio.run_coroutine_threadsafe(
            self.login(email, password, max_tries, user_agent, login_method, session),
            self.loop,
        )

    async def _get(self, url: str, params: dict[str, str]):
        if not self.state:
            raise PhoenixError("Not yet logged in!")
        return self.state.get(url, params)

    async def _post(self, url: str, params: dict[str, str]):
        if not self.state:
            raise PhoenixError("Not yet logged in!")
        return self.state.get(url, params)

    async def _payload_post(self, url: str, params: dict[str, str]):
        if not self.state:
            raise PhoenixError("Not yet logged in!")
        return self.state.get(url, params)

    async def _graphql(self, *queries):
        # TODO - typing
        if not self.state:
            raise PhoenixError("Not yet logged in!")
        return tuple(self.state.graphql_requests(*queries))

    async def logged_in(self) -> bool:
        if not self.state:
            raise PhoenixError("Not yet logged in!")
        return self.state.is_logged_in()

    async def login(
        self, email, password, max_tries, user_agent, login_method, session
    ):
        events.handle_event("loginBegin", email)
        if max_tries < 1:
            raise PhoenixError("Cannot login with max_tries smaller than 1.")

        if not (email and password):
            raise PhoenixError("Email and password not set.")

        for i in range(1, max_tries + 1):
            try:
                if login_method == LoginMethod.SESSION:
                    # TODO - login using premade session
                    self.state = await State.login_session(session)
                elif login_method == LoginMethod.REST:
                    self.state = await State.login(
                        email,
                        password,
                        events.get_handler("2fa"),
                        user_agent=user_agent,
                    )
                elif login_method == LoginMethod.WEBDRIVER:
                    self.state = State.login_selenium(
                        email,
                        password,
                        events.get_handler("2fa"),
                        user_agent=user_agent,
                    )
                else:
                    raise PhoenixError("Unknown login method.")
                self.uid = self.state.user_id
            except PhoenixError:
                if i >= max_tries:
                    raise
                logutils.error(f"Attempt #{i} failed. Retrying after 1s delay.")
                await asyncio.sleep(1)
            else:
                events.handle_event("loginSuccess", email)
                break

    async def logout(self) -> bool:
        """Safely log out the client."""

        if await self.state.logout():
            self.state = None
            self.uid = None
            return True
        return False

    @property
    def thread(self) -> Thread:
        """Check if thread ID is given and if default is set, and return correct values."""
        return Thread(self.default_thread_id, self.default_thread_type)

    @thread.setter
    def thread(self, new_value: Thread | (int, str | ThreadType)):
        if isinstance(new_value, Thread):
            self.default_thread_id = new_value.thread_id
            self.default_thread_type = new_value.thread_type
        elif isinstance(new_value, tuple):
            self.default_thread_id = new_value[0]
            if isinstance(new_value[1], str):
                self.default_thread_type = new_value[1]
            elif isinstance(new_value[1], ThreadType):
                self.default_thread_type = new_value[1].value
            else:
                raise PhoenixError("Invalid thread type.")
        else:
            raise PhoenixError("Invalid thread type.")

    def reset_thread(self):
        self.default_thread_id = None
        self.default_thread_type = None


