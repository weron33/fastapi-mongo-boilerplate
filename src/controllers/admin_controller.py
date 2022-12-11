from http import HTTPStatus

from src.services import admin_service


def migrate_database_controller(collections: list, migrate_to: str, **kwargs) -> dict and HTTPStatus:
    customer_db_code = kwargs.pop('customer_db_code')
    migration_status = admin_service.migrate_service(collection_names=collections,
                                                     migrate_to=migrate_to,
                                                     customer_db_code=customer_db_code)
    if any(migration_status.values()):
        code = HTTPStatus.CREATED
        result = {
            'msg': code.phrase,
            'data': migration_status,
            'code': code
        }
    else:
        code = HTTPStatus.CONFLICT
        result = {
            'msg': 'All collections in target database contains the same data as main database.'
                   'Migration isn\'t necessary.',
            'data': migration_status,
            'code': code
        }
    return result, code


def dump_collections_controller(collections: list, **kwargs) -> dict and HTTPStatus:
    customer_db_code = kwargs.pop('customer_db_code') if 'customer_db_code' in kwargs else None
    admin_service.dump_service(collections, customer_db_code)
    code = HTTPStatus.CREATED
    result = {
        'msg': code.phrase,
        'code': code
    }
    return result, code


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
