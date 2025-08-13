from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from core.config import config


class MongoDB:
    def __init__(self):
        self.client: MongoClient | None = None
        self.db = None

    def connect(self) -> "MongoDB":
        """Connect to MongoDB using settings from .env"""
        try:
            self.client = MongoClient(config.mongo_uri, config.mongo_port)
        except ConnectionFailure as error:
            raise ConnectionError(
                f"Failed to connect to MongoDB at '{config.mongo_uri}': {error}"
            )

        self.db = self.client[config.mongo_db]
        return self

    def get_collection(self, collection_name: str):
        """Retrieve a collection by name from config"""
        if collection_name not in config.mongo_collections:
            raise ValueError(
                f"Invalid collection name '{collection_name}'. "
                f"Must be one of: {list(config.mongo_collections.keys())}"
            )
        return self.db[config.mongo_collections[collection_name]]

    def create_document(self, collection_name: str, document: dict) -> str:
        """Insert a single document and return inserted ID"""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def create_documents(
        self, collection_name: str, documents: list[dict]
    ) -> list[str]:
        """Insert multiple documents and return list of inserted IDs"""
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return [str(_id) for _id in result.inserted_ids]

    def read_documents(
        self, collection_name: str, query: dict = None, projection: dict = None
    ) -> list[dict]:
        """Find documents matching a query"""
        collection = self.get_collection(collection_name)
        return list(collection.find(query or {}, projection))

    def update_documents(
        self, collection_name: str, query: dict, update: dict, many: bool = False
    ) -> int:
        """Update documents matching a query"""
        collection = self.get_collection(collection_name)
        if many:
            result = collection.update_many(query, {"$set": update})
        else:
            result = collection.update_one(query, {"$set": update})
        return result.modified_count

    def delete_documents(
        self, collection_name: str, query: dict, many: bool = False
    ) -> int:
        """Delete documents matching a query"""
        collection = self.get_collection(collection_name)
        if many:
            result = collection.delete_many(query)
        else:
            result = collection.delete_one(query)
        return result.deleted_count
