from mylib.logic.dataclass_serializer import DataclassSerializer
import mylib.logic.aes as aes
import os
from .constants import Constants
from .data.config_data import *


class ConfigManager:
    General: GeneralConfig = GeneralConfig()
    Encrypted: EncryptedConfig = EncryptedConfig()

    def __init__(self, password):
        self.password = password

    def load(self):
        if not os.path.exists(Constants.GENERAL_CONFIG_PATH):
            DataclassSerializer.serialize(ConfigManager.General, Constants.GENERAL_CONFIG_PATH)
        if not os.path.exists(Constants.ENCRYPTED_CONFIG_PATH):
            DataclassSerializer.serialize_with_encrypt(ConfigManager.Encrypted, Constants.ENCRYPTED_CONFIG_PATH, self.password)
        ConfigManager.General = DataclassSerializer.deserialize(GeneralConfig, Constants.GENERAL_CONFIG_PATH)
        ConfigManager.Encrypted = DataclassSerializer.deserialize_with_decrypt(EncryptedConfig, Constants.ENCRYPTED_CONFIG_PATH, self.password)

    def save(self):
        DataclassSerializer.serialize(ConfigManager.General, Constants.GENERAL_CONFIG_PATH)
        DataclassSerializer.serialize_with_encrypt(ConfigManager.Encrypted, Constants.ENCRYPTED_CONFIG_PATH, self.password)

    def decrypt(self):
        aes.AES(self.password).decrypt_file(Constants.ENCRYPTED_CONFIG_PATH)

    def encrypt(self):
        aes.AES(self.password).encrypt_file(Constants.ENCRYPTED_CONFIG_PATH)
