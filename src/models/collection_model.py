import json
import os

from src.models.connection_model import MongoConnection


class MongoCollection:
    """
    Creates (or connects to) MongoDB collection using specified schema.
    In additional creates (or connects to) archive collection where the previous versions of documents are stored.
    """

    INIT_SUFFIX: str = '.init.json'
    ARCHIVE_SUFFIX: str = '_arch'
    VALIDATOR_FILE_SUFFIX: str = '_validator.json'

    def __init__(self,
                 conn: MongoConnection,
                 database_name: str,
                 collection_name: str,
                 validators_path: str,
                 migration_database: str = None,
                 verbose: bool = True):

        self.client = conn.client
        self.init_path = conn.init_path
        self.validators_path = validators_path
        self.database_name = database_name
        self.db = self.client[migration_database] if migration_database else self.client[self.database_name]
        self.name = collection_name
        self.name_arch = f"{self.name}{self.ARCHIVE_SUFFIX}"
        collections = self.db.list_collection_names()

        # Current database state
        if self.name not in collections:
            # Creates collection of current state using validator stored in ./src/validators/
            with open(f"{self.validators_path}/{self.name}{self.VALIDATOR_FILE_SUFFIX}", 'r') as validator:
                self.collection = self.db.create_collection(self.name, validator=json.load(validator))
                if verbose:
                    print(f'Collection \'{self.name}\' in database \'{self.db.name}\' created successfully!')
            self._initialize_data()
        else:
            # This case applies if collection already exists, so validator will be updated (in case of any changes)
            # and collection connection will be established.
            validator_filename = f"{self.validators_path}/{self.name}{self.VALIDATOR_FILE_SUFFIX}"
            if os.path.exists(validator_filename):
                with open(validator_filename, 'r') as validator:
                    self.db.command({"collMod": self.name, "validator": json.load(validator)})  # Validator update
                    self.collection = self.db[self.name]
                    if verbose:
                        print(f'Collection \'{self.name}\' in database \'{self.db.name}\' already created')

        # Archive collection
        if self.name_arch not in collections:
            # If archive collection doesn't exist
            # No validator included, because archive can store all versions of documents,
            # regardless of validators their apply to.
            self.collection_arch = self.db.create_collection(f'{self.name_arch}')
            if verbose:
                print(f'Collection \'{self.name_arch}\' in database \'{self.db.name}\' created successfully!')
        else:
            # If archive collection exists
            self.collection_arch = self.db[self.name_arch]
            if verbose:
                print(f'Collection \'{self.name_arch}\' in database \'{self.db.name}\' already created')

    def _initialize_data(self):
        data_path = f"{self.init_path}/{self.database_name}/{self.collection.name}{self.INIT_SUFFIX}"
        if os.path.exists(data_path):
            with open(data_path) as data:
                self.collection.insert_many(json.load(data))
        return

    def set_client_db(self, database_name: str) -> None:
        pass

    def set_collection(self, collection_name, migration_database=None):
        pass

    def create(self, docList):
        # TODO: Ogarnąć to ładniej, bo to jest brzydko
        exists = [self.collection.find_one(docObj, {'_id': False}) for docObj in docList
                  if self.collection.find_one(docObj, {'_id': False})]
        docList = [dict(doc, **{'version': 1}) for doc in docList if doc not in exists]
        if docList:
            self.collection.insert_many(docList)
            self._move_to_arch(docList)
            return
        else:
            raise FileExistsError('Documents already exists!')

    def find(self, docObj):
        return self.collection.find(docObj, {'_id': False})

    def delete(self, docObj):
        exists = self.collection.find_one(docObj)
        if exists:
            return self.collection.delete_one(docObj)
        else:
            raise FileNotFoundError('Document with provided data does not exists')

    def update(self, docObj, searchingObj):
        updatedDoc = self.collection.find_one_and_update(searchingObj, {'$set': docObj, '$inc': {'version': 1}})
        if updatedDoc:
            return self._move_to_arch(updatedDoc)
        else:
            raise FileNotFoundError('Document with provided data does not exists')

    def query(self, query):
        return self.collection.find(query)

    def aggregate(self, query):
        return self.collection.aggregate(query)

    def purge(self):
        self.collection.delete_many({})
        self.collection_arch.delete_many({})

    def _move_to_arch(self, docs: dict or list):
        docs = [docs] if type(docs) is dict else docs
        _ = [doc.pop('_id', None) for doc in docs]
        self.collection_arch.insert_many(docs)
        return
