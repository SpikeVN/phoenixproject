import dataclasses
import enum

import attr


@attr.s(cmp=True)
class ThreadType(enum.Enum):
    GROUP = "group"
    USER = "user"

    def __str__(self):
        return self.value


@attr.s(cmp=True)
@dataclasses.dataclass
class Thread:
    thread_id: int
    thread_type: ThreadType
