import json
import os

from src.models.collection_model import settings


def dump_collection(collection, date):
    data = collection.find({})
    data_arch = collection.collection_arch.find({}, {'_id': False})
    path = f"{settings.DUMPS_PATH}/{collection.db.name}"
    backups_path = f"{settings.DUMPS_PATH}/backups/{date}/{collection.db.name}"

    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(backups_path):
        os.makedirs(backups_path)

    data = list(data)
    data_arch = list(data_arch)

    json_object = json.dumps(data)
    json_object_arch = json.dumps(data_arch)

    with open(f'{path}/{collection.name}.json', 'w') as f:
        f.write(json_object)

    with open(f'{backups_path}/{collection.name}.json', 'w') as f:
        f.write(json_object)

    with open(f'{path}/{collection.collection_arch.name}.json', 'w') as f:
        f.write(json_object_arch)

    with open(f'{backups_path}/{collection.collection_arch.name}.json', 'w') as f:
        f.write(json_object_arch)
    return data
