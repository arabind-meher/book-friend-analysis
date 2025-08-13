import uuid
from typing import List, Optional, Iterable
from pydantic import BaseModel, Field
from pymongo import ASCENDING
from pymongo.collection import Collection

from db import MongoDB

COLLECTION_KEY = "users_rating"


class BookRating(BaseModel):
    book_id: str
    rating: float = Field(..., ge=0, le=5)


class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    ratings: List[BookRating] = []

    @staticmethod
    def _coll(mongo: MongoDB) -> Collection:
        return mongo.get_collection(COLLECTION_KEY)

    @classmethod
    def ensure_indexes(cls, mongo: MongoDB) -> None:
        coll = cls._coll(mongo)
        coll.create_index([("user_id", ASCENDING)], unique=True)
        coll.create_index([("username", ASCENDING)], unique=True, sparse=True)

    @classmethod
    def get_by_username(cls, mongo: MongoDB, username: str) -> Optional["User"]:
        doc = cls._coll(mongo).find_one({"username": username})
        return cls(**doc) if doc else None

    @classmethod
    def create(cls, mongo: MongoDB, username: str) -> "User":
        user = cls(username=username)
        cls._coll(mongo).insert_one(user.dict())
        return user

    @classmethod
    def get_or_create_by_username(cls, mongo: MongoDB, username: str) -> "User":
        user = cls.get_by_username(mongo, username)
        if user is None:
            user = cls.create(mongo, username)
        return user

    def add_ratings(self, mongo: MongoDB, items: Iterable[BookRating]) -> None:
        coll = self._coll(mongo)
        coll.update_one(
            {"user_id": self.user_id},
            {"$push": {"ratings": {"$each": [i.dict() for i in items]}}},
        )
        self.ratings.extend(items)
