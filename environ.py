import os
from dotenv import load_dotenv
import logging


class EnvFile:

    @staticmethod
    def Get(key: str, defaultValue: any) -> any:
        try:
            load_dotenv()
            return os.environ[key]
        except KeyError:
            logging.warning(
                f"{key} not found in .env file. Using default value: {defaultValue}")
            print(
                f"{key} not found in .env file. Using default value: {defaultValue}")
            return defaultValue
