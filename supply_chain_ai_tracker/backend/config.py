"""Configuration settings for the Supply Chain AI Tracker backend.

Uses Pydantic's BaseSettings to pull values from environment variables with sensible defaults.
"""

from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # MongoDB connection URI
    mongo_uri: str = Field(default="mongodb://localhost:27017", env="MONGO_URI")
    mongo_db_name: str = Field(default="supply_chain", env="MONGO_DB_NAME")

    # Kafka settings
    kafka_bootstrap_servers: str = Field(default="localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic: str = Field(default="transit_updates", env="KAFKA_TOPIC")
    kafka_group_id: str = Field(default="supply-chain-consumer", env="KAFKA_GROUP_ID")

    # OpenAI API key – optional
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")

    # Server settings
    fastapi_host: str = Field(default="0.0.0.0", env="FASTAPI_HOST")
    fastapi_port: int = Field(default=8000, env="FASTAPI_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
