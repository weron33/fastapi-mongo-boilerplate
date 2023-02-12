from fastapi import APIRouter

from src.controllers import admin_controller
from src.schemas.requests import MigrateRequestBody
from src.schemas.responses import NotFoundResponse, SuccessResponse, CreatedResponse, ConflictResponse, \
    NotModifiedResponse

router = APIRouter(tags=['admin'])


@router.post('/admin/migrate')
async def _migrate_route(fromDatabase: str, toDatabase: str,
                         body: MigrateRequestBody) -> CreatedResponse or ConflictResponse:
    collections = body.collections
    response = admin_controller.migrate_database_controller(fromDatabase, toDatabase, collections)
    return response


@router.post('/admin/dump/{databaseName}')
async def _dump_route(databaseName: str, body: MigrateRequestBody):
    collections = body.collections
    response = admin_controller.dump_collections_controller(collections=collections, database_name=databaseName)
    return response
