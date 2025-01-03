from helpers import singleton
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from .environment import EnvVarConfig
from .database import get_database


@singleton
class AppConfig():
    def __init__(self):
        self.env: EnvVarConfig = EnvVarConfig()
        self.db: AsyncIOMotorDatabase = get_database(self.env)


def get_config():
    return AppConfig()
