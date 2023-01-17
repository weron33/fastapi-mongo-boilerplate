from http import HTTPStatus

from src.schemas.responses import SuccessResponse, NotFoundResponse, ConflictResponse, CreatedResponse, \
    NotModifiedResponse
from src.services import collection_service


def get_docs(**kwargs) -> NotFoundResponse or SuccessResponse:
    docs = collection_service.get_doc(**kwargs)
    docs = list(docs)
    if docs is None or docs == []:
        response = NotFoundResponse()
    else:
        response = SuccessResponse(docs)
    return response


def post_doc(docs: list, **kwargs) -> CreatedResponse or ConflictResponse:
    try:
        collection_service.post_doc(docs, **kwargs)
        response = CreatedResponse()
    except FileExistsError:
        response = ConflictResponse()
    return response


def delete_docs(**kwargs) -> SuccessResponse or NotFoundResponse or NotModifiedResponse:
    if not kwargs:
        response = NotModifiedResponse()
    else:
        try:
            collection_service.delete_doc(**kwargs)
            response = SuccessResponse(items=[])
        except FileNotFoundError:
            response = NotFoundResponse()
    return response


def update_doc(doc_obj: dict, **kwargs) -> SuccessResponse or NotFoundResponse:
    try:
        collection_service.update_doc(doc_obj, **kwargs)
        response = SuccessResponse(items=[])
    except FileNotFoundError:
        response = NotFoundResponse()
    return response


def get_many_docs(**kwargs) -> SuccessResponse or NotFoundResponse:
    docs = collection_service.get_many_docs(**kwargs)
    docs = list(docs)
    if docs is None or docs == []:
        response = NotFoundResponse()
    else:
        response = SuccessResponse(items=docs)
    return response


def query_docs(query: dict or list, **kwargs) -> SuccessResponse or NotFoundResponse:
    docs = collection_service.query_docs(query, **kwargs)
    docs = list(docs)
    if docs is None or docs == []:
        response = NotFoundResponse()
    else:
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            response = SuccessResponse
    return response
