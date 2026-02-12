from typing import Any, ClassVar, Protocol

from sqlalchemy import Row


class Dataclass(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]


def dataclass_from_row[D: Dataclass](*, cls: type[D], row: Row) -> D:
    d = {field: getattr(row, field) for field in cls.__dataclass_fields__.keys()}
    return cls(**d)
