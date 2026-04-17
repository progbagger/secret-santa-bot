from dataclasses import dataclass

from secret_santa_bot.helpers.with_id import WithId
from secret_santa_bot.repositories.postgres.tables import users

@dataclass
class CreateUser(WithId[int]):
    
