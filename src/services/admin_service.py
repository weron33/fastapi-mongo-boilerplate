from datetime import datetime
from typing import Dict

from src.configs.config import settings
from src.services.utils.databases_connections_util import choose_database
from src.services.utils.admin_utils import dump_collection


def migrate_service(from_database: str, to_database: str, collection_names: list) -> Dict[str, bool]:
    migration_status = {}
    date_format = "%Y-%m-%dT%H-%M-%S"
    init_date = datetime.now().strftime(date_format)
    for collection_name in collection_names:
        source_database = choose_database(database_name=from_database)
        source_collection = settings.MONGO_DATABASES[source_database][collection_name]
        data = source_collection.find({})

        target_database = choose_database(database_name=to_database, migrate_collections=collection_names)
        target_collection = settings.MONGO_DATABASES[target_database][collection_name]
        # Creating database dump just in case
        dump_collection(target_collection, init_date)
        try:
            target_collection.purge()
            target_collection.create(list(data))
            migration_status[collection_name] = True
        except FileExistsError:
            migration_status[collection_name] = False
    return migration_status


def dump_service(collection_names: list, database_name=None) -> None:
    date_format = "%Y-%m-%d-%H-%M-%S"
    init_date = datetime.now().strftime(date_format)
    customer_db_code = choose_database(database_name=database_name)
    for collection_name in collection_names:
        collection = settings.MONGO_DATABASES[customer_db_code][collection_name]
        _ = dump_collection(collection, init_date)


def create_database_service(database_name: str = None) -> str:
    return choose_database(database_name)


def get_databases_service() -> list:
    conn = settings.MONGO_CONNECTION
    return conn.get_customer_databases()
