from dataclasses import dataclass
from datetime import datetime


@dataclass
class WithCreatedAt:
    created_at: datetime


@dataclass
class WithUpdatedAt:
    updated_at: datetime


@dataclass
class WithTimeTracking(WithUpdatedAt, WithCreatedAt): ...
