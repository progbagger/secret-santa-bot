from dataclasses import dataclass


@dataclass
class WithId[T]:
    id: T
