from .db_manager import DBManager
from .config_manager import ConfigManager
from dataclasses import dataclass


@dataclass
class SharedContext:
    DB: DBManager
    Config: ConfigManager

    def __init__(self, password):
        self.Config = ConfigManager(password)
        self.Config.load()

    def initialize_db(self):
        self.DB = DBManager(self.Config.Encrypted.db_name,
                            self.Config.Encrypted.db_user,
                            self.Config.Encrypted.db_pass,
                            self.Config.Encrypted.db_host,
                            self.Config.Encrypted.db_port)


class SharedLogic:

    @staticmethod
    def initialize(password):
        pass
