
from enum import Enum, auto


class DatabaseActionType(Enum):
    WRITE_DATA_STORAGE = auto()  # Writes do not require a response on the request

