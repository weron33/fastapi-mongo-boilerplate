from fastapi import APIRouter, Request

from src.controllers import collection_controller
from src.schemas.requests import PostRequestBody, PutRequestBody, QueryRequestBody
from src.schemas.responses import NotFoundResponse, SuccessResponse, CreatedResponse, ConflictResponse, \
    NotModifiedResponse

router = APIRouter(tags=['collection'])


@router.get('/api/{database}/{collection}/{docId}')
async def _get_document(database: str, collection: str, docId: str) -> NotFoundResponse or SuccessResponse:
    """
    This route was created to provide quick and easy access to certain document.
    By applying docId one can simply take out document from given collection from given database.
    :param database: name of database to connect
    :param collection: name of collection in given database
    :param docId: id of the document
    :return: response of type NotFoundResponse or SuccessResponse according to result of controller
    """
    return collection_controller.get_docs(database=database, collection=collection, name=docId)


@router.post('/api/{database}/{collection}')
async def _post_document(body: PostRequestBody, database: str, collection: str) -> CreatedResponse or ConflictResponse:
    """
    Posts document(s) into called collection in called database.
    The given list of objects gonna be inserted into collection after passing validation.
    In case exactly the same document already exists in database, it will be removed from passed list.
    :param body: body of the request
    :param database: name of database to connect
    :param collection: name of collection in given database
    :return: response of type CreatedResponse or ConflictResponse according to result of controller
    """
    docs = body.docs
    return collection_controller.post_doc(docs, database=database, collection=collection)


@router.put('/api/{database}/{collection}')
async def _put_document(body: PutRequestBody, database: str, collection: str, request: Request) -> SuccessResponse or NotFoundResponse:
    """
    Updates queried document as provided in body.
    Query of the document is taken from params, body contains the method to change values of document
    :param body: body of the request
    :param database: name of database to connect
    :param collection: name of collection in given database
    :param request: variable to get query params
    :return: response of type SuccessResponse or NotFoundResponse according to result of controller
    """
    doc_obj = body.doc
    params = request.query_params
    return collection_controller.update_doc(doc_obj, database=database, collection=collection, **params)


@router.delete('/api/{database}/{collection}')
async def _delete_document(database: str, collection: str, request: Request) -> SuccessResponse or NotFoundResponse or NotModifiedResponse:
    """
    Deletes document from collection in database according to provided params
    :param database: name of database to connect
    :param collection: name of collection in given database
    :param request: variable to get query params
    :return:
    """
    params = request.query_params
    return collection_controller.delete_docs(database=database, collection=collection, **params)


@router.get('/api/{database}/{collection}')
async def _get_many_documents(database: str, collection: str, request: Request) -> NotFoundResponse or SuccessResponse:
    """
    Queries documents according to provided params.
    By applying docId one can simply take out document from given collection from given database.
    :param database: name of database to connect
    :param collection: name of collection in given database
    :param request: variable to get query params
    :return: response of type NotFoundResponse or SuccessResponse according to result of controller
    """
    params = request.query_params
    return collection_controller.get_many_docs(database=database, collection=collection, **params)


@router.post('/api/{database}/{collection}/query')
async def _query_document(body: QueryRequestBody, database: str, collection: str) -> SuccessResponse or NotFoundResponse:
    """
    Route to enable native query to MongoDB in case of more complicated cases.
    :param body: body of the request
    :param database: name of database to connect
    :param collection: name of collection in given database
    :return: response of type NotFoundResponse or SuccessResponse according to result of controller
    """
    query = body.query
    return collection_controller.query_docs(query, database=database, collection=collection)
