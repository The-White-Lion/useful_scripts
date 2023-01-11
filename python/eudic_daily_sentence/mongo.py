import sys
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.collection import Collection


class MongoContextManager:
    """Managing resource with context manager"""

    def __init__(self, connect_string: str, db_name: str) -> None:
        self.connect_string = connect_string
        self.db_name = db_name
        self.client = None
        self.logger = logging.getLogger("eudic.mongodb")

    def __enter__(self) -> "MongoContextManager":
        try:
            self.client = MongoClient(self.connect_string)
        except PyMongoError as exception:
            self.logger.error("mongodb connection faliure: %s", exception)
            sys.exit(1)
        return self

    def __exit__(self, exception_type, exception_val, traceback):
        if exception_type:
            self.logger.error("An error occurred: %s", exception_type)
            self.logger.error("reason: %s", exception_val)
            self.logger.error("traceback: %s", traceback)
        self.client.close()

    def __get_collection(self, collection_name: str) -> Collection:
        """get mongodb collection"""

        database = self.client[self.db_name]
        collection = database[collection_name]
        return collection


    def create(self, collection_name: str, data: dict) -> list:
        """insert record into specified mongodb collection"""

        collection = self.__get_collection(collection_name)
        result = collection.insert_many([data])
        return result.inserted_ids

    def delete(self, collection_name: str, filters: dict) -> int:
        """delete record from specified mongodb collection"""

        collection = self.__get_collection(collection_name)
        result = collection.delete_many(filters)
        return result.deleted_count

    def update(self, collection_name: str, data: list) -> int:
        """update record in mongodb collection"""

        collection = self.__get_collection(collection_name)
        result = collection.update_many(*data)
        return result.modified_count

    def retrieve(self, collection_name: str, filters: dict = None) -> list:
        """query record in mongodb collection with given filters condition"""

        if filters is None:
            filters = {}

        collection = self.__get_collection(collection_name)
        cursor = collection.find(filters)
        result = []
        for document in cursor:
            result.append(document)
        return result
