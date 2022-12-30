from fastapi import APIRouter, Request

from src.controllers import collection_controller

router = APIRouter()


@router.get('/api/{database}/{collection}/{docId}')
async def _get_document(database: str, collection: str, docId: str):
    return collection_controller.get_docs(database=database, collection=collection, name=docId)


@router.post('/api/{database}/{collection}')
async def _post_document(request: Request, database: str, collection: str):
    body = await request.json()
    docs = body['doc']
    return collection_controller.post_doc(docs, database=database, collection=collection)


@router.put('/api/{database}/{collection}')
async def _put_document(request: Request, database: str, collection: str):
    body = await request.json()
    doc_obj = body['doc']
    params = request.query_params
    return collection_controller.update_doc(doc_obj, database=database, collection=collection, **params)


@router.delete('/api/{database}/{collection}')
async def _delete_document(request: Request, database: str, collection: str):
    params = request.query_params
    return collection_controller.delete_docs(database=database, collection=collection, **params)


@router.get('/api/{database}/{collection}')
async def _get_many_documents(request: Request, database: str, collection: str):
    params = request.query_params
    return collection_controller.get_many_docs(database=database, collection=collection, **params)


@router.post('/api/{database}/{collection}/query')
async def _query_document(request: Request, database: str, collection: str):
    body = await request.json()
    query = body['doc']
    return collection_controller.query_docs(query, database=database, collection=collection, **params)
