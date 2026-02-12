from contextvars import ContextVar
from dataclasses import dataclass

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class PostgresError(Exception): ...


class NoActiveConnectionError(PostgresError): ...


@dataclass
class Credentials:
    username: str = "postgres"
    password: str = "postgres"
    database: str = "postgres"
    host: str = "0.0.0.0"
    port: int = 5432

    def url(self) -> sa.URL:
        return sa.URL.create(
            drivername="sqlalchemy+asyncpg",
            username=self.username,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port,
        )


class ConnectionError(PostgresError):
    def __init__(self, creds: Credentials) -> None:
        super().__init__("Unable to connect", creds)


_sessionmaker: async_sessionmaker | None = None
_session: ContextVar[AsyncSession] = ContextVar("pg_session")


def get() -> AsyncSession:
    if _sessionmaker is None:
        raise NoActiveConnectionError

    global _session
    try:
        return _session.get()
    except LookupError:
        _session.set(session := _sessionmaker())
        return session


def connect(creds: Credentials) -> None:
    try:
        engine = create_async_engine(creds.url())

        global _sessionmaker
        _sessionmaker = async_sessionmaker(engine)
    except Exception as e:
        raise ConnectionError(creds) from e
