from injector import Module, provider, singleton
from loguru import logger

from settings import Settings
from src.database.adapters.mongodb_adapter import MongoDBAdapter
from src.database.interfaces.mongodb_port import MongoDBPort
from src.providers.dummy_json_client import DummyJsonClient
from src.providers.http_client import HttpClient


class AppContainer(Module):
    @singleton
    @provider
    def provide_settings(self) -> Settings:
        return Settings()

    @singleton
    @provider
    def provide_database(self, settings: Settings) -> MongoDBPort:
        logger.info("Conexão MongoDB configurada")
        return MongoDBAdapter(
            settings.MONGODB_CONNECTION_STRING,
            settings.MONGODB_DB_NAME,
        )

    @singleton
    @provider
    def provide_http_client(self) -> HttpClient:
        return HttpClient()

    @singleton
    @provider
    def provide_dummy_json_client(self, http_client: HttpClient, settings: Settings) -> DummyJsonClient:
        return DummyJsonClient(http_client, settings.BIRTH_DATE_API_URL)
