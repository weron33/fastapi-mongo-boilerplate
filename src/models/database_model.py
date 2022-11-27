class MongoDatabase:
    """
    Creates (or connects to) MongoDB database.
    """

    def __init__(self, conn, database_name: str, archive_suffix: str):
        self.client = conn.client
        self.database_name = database_name
        self.db = self.client[self.database_name]
        self.collections_names = self.db.list_collection_names()
        self.collections_names = [x for x in self.collections_names if archive_suffix not in x]
        print(f"Connecting to database: {self.database_name}")
