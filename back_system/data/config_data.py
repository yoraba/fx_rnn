from dataclasses import dataclass
from datetime import datetime

@dataclass
class GeneralConfig:
    start_date: str = '1970-1-1'

@dataclass
class EncryptedConfig:
    db_name: str = ''
    db_user: str = ''
    db_pass: str = ''
    db_host: str = ''
    db_port: int = 0
    quandl_token: str = ''