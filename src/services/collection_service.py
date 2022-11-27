from flask import current_app, request

from src.models.collection_model import MongoCollection
from src.services.utils.set_db import choose_database
from src.services.utils.verification_util import remove_duplicates_from_intput


def get_doc(**kwargs):
    collection, kwargs = _get_collection(**kwargs)
    result = collection.find(kwargs)
    return result


def post_doc(doc_list: list, **kwargs):
    doc_list = remove_duplicates_from_intput(doc_list)
    collection, kwargs = _get_collection(**kwargs)
    return collection.create(doc_list)


def delete_doc(**kwargs):
    collection, kwargs = _get_collection(**kwargs)
    result = collection.delete(kwargs)
    return result


def update_doc(doc_obj: dict, **kwargs):
    collection, kwargs = _get_collection(**kwargs)
    result = collection.update(doc_obj, kwargs)
    return result


def get_all_docs(**kwargs):
    collection, kwargs = _get_collection(**kwargs)
    query = {}
    result = collection.find(query)
    return result


def query_docs(query: dict or list, **kwargs):
    collection, kwargs = _get_collection(**kwargs)
    result = collection.query(query)
    return result


def aggregate_docs(query: dict or list, **kwargs):
    collection, kwargs = _get_collection(**kwargs)
    result = collection.aggregate(query)
    return result


def _get_collection(**kwargs) -> MongoCollection and dict:
    customer_db_code = choose_database(kwargs.pop('customer_db_code') if 'customer_db_code' in kwargs else None)
    return current_app.config[customer_db_code][request.blueprint], kwargs

