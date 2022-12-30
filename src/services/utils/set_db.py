import json
import os

from src.configs.config import settings
from src.models.collection_model import MongoCollection
from src.models.database_model import MongoDatabase


def choose_database(database_name: str = None) -> str:
    return settings.connect_database(database_name)


# def connect_database(database_name: str) -> str:
#     def _create_collections(database_name: str, collections_list: list) -> None:
#         conn = current_app.config['MONGO_CONNECTION']
#         if collections_list:
#             for collection_name in collections_list:
#                 current_app.config[database_name][collection_name] = MongoCollection(conn=conn,
#                                                                                      database_name=database_name,
#                                                                                      collection_name=collection_name,
#                                                                                      verbose=False)
#
#     def _create_client_db(database_name: str, collections_dict: dict) -> None:
#         current_app.config[database_name] = dict()
#         _create_collections(database_name, collections_dict['required'])
#         _create_collections(database_name, collections_dict['missing'])
#         _create_collections(database_name, collections_dict['additional'])
#
#     def _load_required_collection_names(database_name):
#         customer_schema = f"{settings.SCHEMAS_PATH}/{database_name}.json"
#         if not os.path.exists(customer_schema):
#             customer_schema = f"{settings.SCHEMAS_PATH}/customer-db.json"
#         with open(customer_schema, 'r') as f:
#             required_collection_names = json.load(f)
#         return required_collection_names
#
#     def _split_collections(db_colls: list, required: list) -> dict:
#         additional = list(sorted(set(db_colls) - set(required)))
#         missing = list(sorted(set(required) - set(db_colls)))
#         return {'required': required, 'missing': missing, 'additional': additional}
#
#     if database_name not in current_app.config:  # Database is not connected (maybe exists, maybe not)
#         required_collections_filename = _load_required_collection_names(database_name)
#         collections_names = MongoDatabase(database_name).collections_names
#         collections_dict = _split_collections(collections_names, required_collections_filename)
#         _create_client_db(database_name, collections_dict)
#     return database_name
