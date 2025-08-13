from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Config(BaseSettings):
    # Mongo connection
    mongo_uri: str
    mongo_port: int
    mongo_db: str

    # Mongo collections
    mongo_collection_metadata_raw: str
    mongo_collection_metadata_clean: str
    mongo_collection_reviews_raw: str
    mongo_collection_reviews_clean: str
    mongo_collection_users_rating: str
    mongo_collection_sentiment_scores: str
    mongo_collection_summarized_reviews: str

    # PostgreSQL connection
    postgres_url: str
    postgres_schema: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
    )

    @property
    def mongo_collections(self) -> dict[str, str]:
        return {
            "metadata_raw": self.mongo_collection_metadata_raw,
            "metadata_clean": self.mongo_collection_metadata_clean,
            "reviews_raw": self.mongo_collection_reviews_raw,
            "reviews_clean": self.mongo_collection_reviews_clean,
            "users_rating": self.mongo_collection_users_rating,
            "sentiment_scores": self.mongo_collection_sentiment_scores,
            "summarized_reviews": self.mongo_collection_summarized_reviews,
        }


config = Config()
