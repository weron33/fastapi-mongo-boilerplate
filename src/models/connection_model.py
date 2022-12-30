import os

from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoConnection:
    """
    Creates connection MongoDB server.
    """

    settings_DATABASES = ['admin', 'config', 'local']
    STASH_FOLDER = 'stash'

    def __init__(self, url, init_path):
        self.client = MongoClient(url, server_api=ServerApi('1'))
        self.databases_names = self.client.list_database_names()
        self.init_path = init_path
        self.customers_databases_names = None
        for config_database in self.settings_DATABASES:
            if config_database in self.databases_names:
                self.databases_names.remove(config_database)

    def get_customer_databases(self) -> list:
        if self.customers_databases_names:
            return self.customers_databases_names
        else:
            self.customers_databases_names = self.client.list_database_names()
            for config_database in self.settings_DATABASES:
                if config_database in self.customers_databases_names:
                    self.customers_databases_names.remove(config_database)
            return self.customers_databases_names

    def get_missing_databases(self) -> list:
        self.get_customer_databases()
        required_databases = os.listdir(self.init_path)
        if self.STASH_FOLDER in required_databases:
            required_databases.remove(self.STASH_FOLDER)
        missing_databases = list(sorted(set(required_databases) - set(self.databases_names)))
        additional_databases = list(sorted(set(self.databases_names) - set(required_databases)))
        return missing_databases
