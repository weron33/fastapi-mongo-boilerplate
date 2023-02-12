import json
import os

from dotenv import load_dotenv

from src.models.collection_model import MongoCollection
from src.models.connection_model import MongoConnection
from src.models.database_model import MongoDatabase


def _set_env() -> None:
    if os.environ['API_ENV'] == 'development':
        load_dotenv("src/envs/dev-env/.env")
    elif os.environ['API_ENV'] == 'docker':
        load_dotenv("src/envs/docker-env/.env")


class Config:
    _set_env()

    API_HOST = os.environ.get('API_HOST')
    API_PORT = int(os.environ.get('API_PORT'))
    MONGO_URL = os.environ.get('MONGO_URL')
    VALIDATORS_PATH = os.environ.get('VALIDATORS_PATH')
    VALIDATOR_FILE_SUFFIX = os.environ.get('VALIDATOR_FILE_SUFFIX')
    ARCHIVE_SUFFIX = os.environ.get('ARCHIVE_SUFFIX')
    INIT_PATH = os.environ.get('INIT_PATH')
    INIT_SUFFIX = os.environ.get('INIT_SUFFIX')
    SCHEMAS_PATH = os.environ.get('SCHEMAS_PATH')
    DUMPS_PATH = os.environ.get('DUMPS_PATH')

    MONGO_CONNECTION = MongoConnection(MONGO_URL, INIT_PATH)
    MONGO_DATABASES = {}

    def establish_connection_with_databases(self) -> None:
        databases_names = self.MONGO_CONNECTION.databases_names
        databases_names = databases_names + self.MONGO_CONNECTION.get_missing_databases()
        for database_name in databases_names:
            self.connect_database(database_name)

    def connect_database(self, database_name: str, migrate_collections: list = None) -> str:
        if database_name not in self.MONGO_DATABASES:  # Database is not connected (maybe exists, maybe not)
            collections_dict = self._split_collections(database_name, migrate_collections)
            self._create_database(database_name, collections_dict)
        return database_name

    def _split_collections(self, database_name: str, migrate_collections: list = None) -> dict:
        if migrate_collections is None:
            migrate_collections = []
        collections_names = MongoDatabase(self.MONGO_CONNECTION, database_name, self.ARCHIVE_SUFFIX).collections_names
        required = self._load_required_collection_names(database_name)
        additional = list(sorted(set(collections_names) - set(required)))
        missing = list(sorted(set(required) - set(collections_names))) + migrate_collections
        return {'required': required, 'missing': missing, 'additional': additional}

    def _load_required_collection_names(self, database_name) -> list:
        database_schema = f"{self.SCHEMAS_PATH}/{database_name}.json"
        if os.path.exists(database_schema):
            with open(database_schema, 'r') as f:
                required_collection_names = json.load(f)
        else:
            required_collection_names = []
        return required_collection_names

    def _create_database(self, database_name: str, collections_dict: dict) -> None:
        self.MONGO_DATABASES[database_name] = dict()
        self._create_collections(database_name, collections_dict['required'])
        self._create_collections(database_name, collections_dict['missing'])
        self._create_collections(database_name, collections_dict['additional'])

    def _create_collections(self, database_name: str, collections_list: list) -> None:
        if collections_list:
            for collection_name in collections_list:
                self.MONGO_DATABASES[database_name][collection_name] = MongoCollection(conn=self.MONGO_CONNECTION,
                                                                                       validators_path=self.VALIDATORS_PATH,
                                                                                       database_name=database_name,
                                                                                       collection_name=collection_name,
                                                                                       verbose=False)


settings = Config()
settings.establish_connection_with_databases()
