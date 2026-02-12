from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from sqlalchemy import insert, select, update

from secret_santa_bot.helpers.dataclass_from_row import dataclass_from_row
from secret_santa_bot.helpers.with_id import WithId
from secret_santa_bot.helpers.with_time_tracking import WithTimeTracking
from secret_santa_bot.repositories.postgres.connection import get as get_pg
from secret_santa_bot.repositories.postgres.tables import addresses, users


@dataclass
class CreateAddress:
    country: str
    city: str
    street: str
    house: str
    apartment: str | None = None
    description: str | None = None


@dataclass
class Address(CreateAddress, WithTimeTracking, WithId[int]): ...


async def create_address(address: CreateAddress) -> Address:
    query = insert(addresses).values(**asdict(address)).returning(addresses)

    row = (await get_pg().execute(query)).fetchone()
    assert row

    return dataclass_from_row(cls=Address, row=row)


async def get_user_address(user_id: int) -> Address | None:
    query = (
        select(addresses)
        .select_from(addresses.join(users, addresses.c.id == users.c.address_id))
        .where(users.c.id == user_id)
    )

    row = (await get_pg().execute(query)).fetchone()

    return dataclass_from_row(cls=Address, row=row) if row else None


async def update_address(*, address_id: int, params: CreateAddress) -> Address:
    query = update(addresses).values(**asdict(params), updated_at=datetime.now(UTC))

    row = (await get_pg().execute(query)).fetchone()
    assert row

    return dataclass_from_row(cls=Address, row=row)
