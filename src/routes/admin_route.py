from fastapi import APIRouter

from src.controllers import admin_controller
from src.schemas.requests import MigrateRequestBody
from src.schemas.responses import NotFoundResponse, SuccessResponse, CreatedResponse, ConflictResponse, \
    NotModifiedResponse

router = APIRouter(tags=['admin'])


@router.post('/admin/migrate')
async def _migrate_route(fromDatabase: str, toDatabase: str, body: MigrateRequestBody) -> CreatedResponse or ConflictResponse:
    collections = body.collections
    result = admin_controller.migrate_database_controller(fromDatabase, toDatabase, collections)
    return result

# @admin.route('/mongo/admin/dump', methods=['POST'])
# @admin.route('/mongo/<customer_db_code>/admin/dump', methods=['POST'])
# async def _dump_route(**kwargs):
#     collections = request.get_json()['collections']
#     result, code = admin_controller.dump_collections_controller(collections=collections, **kwargs)
#     return jsonify(result), code
#
#
# @admin.route('/mongo/admin/databases/<database_type>/<database_name>', methods=['POST'])
# async def _create_database_route(database_type, database_name):
#     if database_type == 'customer':
#         choose_database()
#         response = {
#             'msg': f'Database of type: {database_type} created under the name of {database_name}.',
#             'data': [],
#             'code': 201
#         }
#     elif database_type == 'customer':
#         choose_database(database_name)
#         response = {
#             'msg': f'Database of type: {database_type} created under the name of {database_name}.',
#             'data': [],
#             'code': 201
#         }
#     else:
#         response = {
#             'msg': f'No valid database type provided. Try one of those: {["common", "customer"]}',
#             'data': [],
#             'code': 401
#         }
#     return jsonify(response), response['code']
#
#
# @admin.route('/mongo/admin/databases/customers', methods=['GET'])
# async def _get_databases():
#     response, code = admin_controller.get_databases_controller()
#     return response, code
