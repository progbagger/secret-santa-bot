import sqlalchemy as sa

_metadata = sa.MetaData()


class TIMESTAMPTZ(sa.TIMESTAMP):
    def __init__(self) -> None:
        super().__init__(timezone=True)


session_status = sa.Enum("draft", "planned", "started", "ended", name="session_status")


addresses = sa.Table(
    "addresses",
    _metadata,
    sa.Column("id", sa.BIGINT, primary_key=True),
    sa.Column("country", sa.TEXT, nullable=False),
    sa.Column("city", sa.TEXT, nullable=False),
    sa.Column("street", sa.TEXT, nullable=False),
    sa.Column("house_number", sa.TEXT, nullable=False),
    sa.Column("apartment", sa.TEXT, nullable=True),
    sa.Column("description", sa.TEXT, nullable=True),
    sa.Column("created_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
    sa.Column("updated_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
)


users = sa.Table(
    "users",
    _metadata,
    sa.Column("id", sa.BIGINT, primary_key=True, autoincrement=False),
    sa.Column("login", sa.TEXT, nullable=True, unique=True),
    sa.Column("display_name", sa.TEXT, nullaple=True),
    sa.Column("phone_number", sa.TEXT, nullable=True),
    sa.Column("address_id", sa.BIGINT, sa.ForeignKey("addresses.id"), nullable=True),
    sa.Column("created_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
    sa.Column("updated_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
)

sessions = sa.Table(
    "sessions",
    _metadata,
    sa.Column("id", sa.BIGINT, primary_key=True),
    sa.Column("name", sa.TEXT, nullable=False),
    sa.Column("description", sa.TEXT, nullable=True),
    sa.Column("started_at", TIMESTAMPTZ, nullable=True),
    sa.Column("ended_at", TIMESTAMPTZ, nullable=True),
    sa.Column("status", session_status, nullable=False),
    sa.Column("created_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
    sa.Column("updated_at", TIMESTAMPTZ, nullable=False, server_default=sa.func.now()),
)

pairs = sa.Table(
    "pairs",
    _metadata,
    sa.Column("id", sa.BIGINT, primary_key=True),
    first_user_id := sa.Column(
        "first_user_id", sa.BIGINT, sa.ForeignKey("users.id"), nullable=False
    ),
    second_user_id := sa.Column(
        "second_user_id", sa.BIGINT, sa.ForeignKey("users.id"), nullable=False
    ),
    session_id := sa.Column(
        "session_id", sa.BIGINT, sa.ForeignKey("sessions.id"), nullable=False
    ),
    sa.Index(
        "users_and_session_unique_idx",
        first_user_id,
        second_user_id,
        session_id,
        unique=True,
    ),
)
