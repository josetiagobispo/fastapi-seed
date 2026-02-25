from decouple import config


class Settings:
    APP_NAME: str = config("APP_NAME", default="Leads API")
    ENVIRONMENT: str = config("ENVIRONMENT", default="development")
    ENABLE_SWAGGER: bool = config("ENABLE_SWAGGER", default=True, cast=bool)
    LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")

    MONGODB_CONNECTION_STRING: str = config("MONGODB_CONNECTION_STRING", default="mongodb://localhost:27017")
    MONGODB_DB_NAME: str = config("MONGODB_DB_NAME", default="leads_db")

    BIRTH_DATE_API_URL: str = config("BIRTH_DATE_API_URL", default="https://dummyjson.com/users/1")
    BIRTH_DATE_API_TIMEOUT: int = config("BIRTH_DATE_API_TIMEOUT", default=5, cast=int)

    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    def should_enable_swagger(self) -> bool:
        return self.ENABLE_SWAGGER or self.is_development()
