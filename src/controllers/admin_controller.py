from http import HTTPStatus

from src.schemas.responses import CreatedResponse, ConflictResponse
from src.services import admin_service


def migrate_database_controller(from_database: str, to_database: str, collections: list) -> CreatedResponse:
    migration_status = admin_service.migrate_service(from_database=from_database,
                                                     to_database=to_database,
                                                     collection_names=collections)
    if any(migration_status.values()):
        response = CreatedResponse()
    else:
        response = ConflictResponse()
    return response


def dump_collections_controller(collections: list, database_name: str) -> dict and HTTPStatus:
    backup_path = admin_service.dump_service(collections, database_name)
    response = CreatedResponse(backup=backup_path)
    return response


def create_database_controller(database_type: str, database_name: str = None) -> dict and HTTPStatus:
    if database_type == 'customer':
        admin_service.create_database_service()
        code = HTTPStatus.CREATED
        response = {
            'msg': f'Database of type: {database_type} created under the name of {database_name}.'
        }
    elif database_type == 'customer':
        admin_service.create_database_service(database_name)
        response = {
            'msg': f'Database of type: {database_type} created under the name of {database_name}.'
        }
    else:
        response = {
            'msg': f'No valid database type provided. Try one of those: {["common", "customer"]}'
        }
    response['code'] = code
    return response, code


def get_databases_controller() -> dict and HTTPStatus:
    databases = admin_service.get_databases_service()
    msg = 'Success'
    code = HTTPStatus.OK
    result = {
        'code': code,
        'data': databases,
        'msg': msg,
    }
    return result, code
