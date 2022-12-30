from datetime import datetime
from typing import Dict

from flask import current_app

from src.routes.utils.ratings_util import add_currency
from src.services.utils.set_db import choose_database
from src.services.utils.admin_utils import dump_collection


def migrate_service(collection_names: list, migrate_to: str, customer_db_code: str) -> Dict[str, bool]:
    migration_status = {}
    date_format = "%d-%m-%Y-%H-%M-%S"
    init_date = datetime.now().strftime(date_format)
    for collection_name in collection_names:
        customer_db_code = choose_database(customer_db_code=customer_db_code)
        from_collection = current_app.config[customer_db_code][collection_name]
        data_to_migrate = from_collection.find({})

        if collection_name in ['domestic_ratings', 'extra_services_ratings', 'petrol_costs', 'surcharges',
                               'transborder_ratings']:
            data_to_migrate = add_currency(data_to_migrate)

        migrate_to = choose_database(customer_db_code=migrate_to)
        to_collection = current_app.config[migrate_to][collection_name]
        # Creating database dump just in case
        data = dump_collection(to_collection, init_date)
        try:
            to_collection.purge()
            to_collection.create(list(data_to_migrate))
            migration_status[collection_name] = True
        except FileExistsError:
            migration_status[collection_name] = False
    return migration_status


def dump_service(collection_names: list, customer_db_code=None) -> None:
    date_format = "%Y-%m-%d-%H-%M-%S"
    init_date = datetime.now().strftime(date_format)
    customer_db_code = choose_database(customer_db_code=customer_db_code)
    for collection_name in collection_names:
        collection = current_app.config[customer_db_code][collection_name]
        _ = dump_collection(collection, init_date)
    return


def create_database_service(database_name: str = None) -> str:
    return choose_database(database_name)


def get_databases_service() -> list:
    conn = current_app.config['MONGO_CONNECTION']
    return conn.get_customer_databases()
