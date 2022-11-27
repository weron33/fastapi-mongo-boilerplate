from fastapi import APIRouter, Request

from src.controllers import collection_controller

router = APIRouter()


@router.get('/api/{database}/{collection}')
async def _get_document(database, collection, **kwargs):
    return collection_controller.get_docs(database=database, collection=collection, **kwargs)


@router.post('/api/{database}/{collection}')
async def _post_document(request: Request, database, collection, **kwargs):
    body = await request.json()
    docs = body['doc']
    return collection_controller.post_doc(docs, database=database, collection=collection, **kwargs)


@router.put('/api/{database}/{collection}')
async def _put_document(request: Request, database, collection, **kwargs):
    body = await request.json()
    doc_obj = body['doc']
    return collection_controller.update_doc(doc_obj, database=database, collection=collection, **kwargs)


@router.delete('/api/{database}/{collection}')
async def _delete_document(database, collection, **kwargs):
    return collection_controller.delete_docs(database=database, collection=collection, **kwargs)


@router.get('/api/{database}/{collection}')
async def _get_all_documents(database, collection, **kwargs):
    return collection_controller.get_all_docs(database=database, collection=collection, **kwargs)


@router.post('/api/{database}/{collection}')
async def _query_document(request: Request, database, collection, **kwargs):
    body = await request.json()
    query = body['doc']
    return collection_controller.query_docs(query, database=database, collection=collection, **kwargs)
