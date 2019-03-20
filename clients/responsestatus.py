import enum


class ResponseStatus(enum.Enum):
    SUCCESS = 202
    ERROR = 404
    CONTINUE = 701
