from http import HTTPStatus

from src.services import collection_service


def get_docs(**kwargs) -> dict:
    docs = collection_service.get_doc(**kwargs)
    docs = list(docs)
    if docs is None or docs == []:
        msg = 'Doc does not exist'
        code = HTTPStatus.NOT_FOUND
        docs = []
    else:
        msg = 'Success'
        code = HTTPStatus.OK
    result = {
        'code': code,
        'msg': msg,
        'data': docs
    }
    return result


def post_doc(docs: list or dict, **kwargs) -> dict:
    if type(docs) is dict:
        docs = [docs]
    try:
        collection_service.post_doc(docs, **kwargs)
        msg = 'Success'
        code = HTTPStatus.CREATED
    except FileExistsError:
        msg = 'Docs/Doc already exist/s'
        code = HTTPStatus.CONFLICT
    result = {
        'code': code,
        'msg': msg,
    }
    return result


def delete_docs(**kwargs) -> dict:
    try:
        collection_service.delete_doc(**kwargs)
        msg = 'Success'
        code = HTTPStatus.OK
    except FileNotFoundError:
        msg = 'Doc does not exist'
        code = HTTPStatus.NOT_FOUND
    result = {
        'code': code,
        'msg': msg,
    }
    return result


def update_doc(doc_obj: dict, **kwargs) -> dict:
    try:
        collection_service.update_doc(doc_obj, **kwargs)
        msg = 'Success'
        code = HTTPStatus.OK
    except FileNotFoundError:
        msg = 'Doc does not exist'
        code = HTTPStatus.NOT_FOUND
    result = {
        'code': code,
        'msg': msg,
    }
    return result


def get_all_docs(**kwargs) -> dict:
    docs = collection_service.get_all_docs(**kwargs)
    docs = list(docs)
    if docs is None or docs == []:
        msg = 'Docs are confused'
        code = HTTPStatus.NOT_FOUND
        docs = []
    else:
        msg = 'Success'
        code = HTTPStatus.OK
    result = {
        'code': code,
        'msg': msg,
        'data': docs
    }
    return result


def query_docs(query: dict or list, **kwargs) -> dict:
    docs = collection_service.query_docs(query, **kwargs)
    docs = list(docs)
    if docs is None or docs == []:
        msg = 'Docs are confused'
        code = HTTPStatus.NOT_FOUND
        docs = []
    else:
        msg = 'Success'
        code = HTTPStatus.OK
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
    result = {
        'code': code,
        'msg': msg,
        'data': docs
    }
    return result


def aggregate_docs(query: dict or list, **kwargs) -> dict:
    docs = collection_service.aggregate_docs(query, **kwargs)
    docs = list(docs)
    if docs is None:
        msg = 'Docs are confused'
        code = HTTPStatus.NOT_FOUND
        docs = []
    elif docs == [] and kwargs['postal_code'] is None:
        msg = 'Country is divided on several zones. Please pass postal code to specify the zone'
        code = HTTPStatus.NOT_FOUND
        docs = []
    elif docs == [] and kwargs['postal_code'] is not None:
        msg = 'Whole country belongs to certain zone. Please send request without postal code'
        code = HTTPStatus.NOT_FOUND
        docs = []
    else:
        msg = 'Success'
        code = HTTPStatus.OK
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            del doc['Zones']
    result = {
        'code': code,
        'msg': msg,
        'data': docs
    }
    return result
