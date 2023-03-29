from http import HTTPStatus

from src.schemas.responses import SuccessResponse, NotFoundResponse, ConflictResponse, CreatedResponse, \
    NotModifiedResponse
from src.services import collection_service


def get_docs(**kwargs) -> NotFoundResponse or SuccessResponse:
    """
    Method in assistance of services query database according to provided input.
    Then wrap return of service into API response.
    :param kwargs: parameters of doc to be queried
    :return: API response of data according to result get from database
    """
    docs = collection_service.get_doc(**kwargs)
    docs = list(docs)
    if docs is None or docs == []:
        response = NotFoundResponse()
    else:
        response = SuccessResponse(docs)
    return response


def post_doc(docs: list, **kwargs) -> CreatedResponse or ConflictResponse:
    """
    Method calls services to create object in database. Then creates a valid API response.
    :param docs: Document to create in database
    :param kwargs: Additional parameters
    :return: Valid API response
    """
    try:
        collection_service.post_doc(docs, **kwargs)
        response = CreatedResponse()
    except FileExistsError:
        response = ConflictResponse()
    except KeyError as e:
        response = NotFoundResponse(msg=e)
    return response


def delete_docs(**kwargs) -> SuccessResponse or NotFoundResponse or NotModifiedResponse:
    """
    Method to wrap information about delete process in database into response.
    :param kwargs: Additional parameters, such as database name or collection name
    :return: Valid API response
    """
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
    """
    Method to wrap information about update process in database into response.
    :param doc_obj: The way to update object
    :param kwargs: Parameters to query object
    :return: Valid API response
    """
    try:
        collection_service.update_doc(doc_obj, **kwargs)
        response = SuccessResponse(items=[])
    except FileNotFoundError:
        response = NotFoundResponse()
    return response


def get_many_docs(**kwargs) -> SuccessResponse or NotFoundResponse:
    """
    Method in assistance of services query database according to provided input.
    Then wrap return of service into API response.
    :param kwargs: parameters of doc to be queried
    :return: API response of data according to result get from database
    """
    docs = collection_service.get_many_docs(**kwargs)
    docs = list(docs)
    if docs is None or docs == []:
        response = NotFoundResponse()
    else:
        response = SuccessResponse(items=docs)
    return response


def query_docs(query: dict or list, **kwargs) -> SuccessResponse or NotFoundResponse:
    """
    Method to wrap into response results of native Mongo query.
    :param query: Native MongoDB query
    :param kwargs: Additional parameters
    :return: Valid API response
    """
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
