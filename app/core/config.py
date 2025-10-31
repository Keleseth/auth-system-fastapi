from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # UUID пользователей для проверки прав доступа
    AUTHOR_USER_UUID: str = 'fc32b64f-2599-4dd3-ac28-3a1b3fad4e30'
    AUTHOR_EMAIL: str = 'author@yandex.ru'
    ADMIN_USER_UUID: str = 'c50eb804-131d-4cde-a504-cea137c00dc6'
    ADMIN_EMAIL: str = 'admin@yandex.ru'
    NOT_AUTHOR_USER_UUID: str
    MODERATOR_USER_UUID: str = '4a2b3ad3-e3ca-4f71-89cf-f8907849647b'
    MODERATOR_EMAIL: str = 'moderator@yandex.ru'
    PASSWORD: str = 'password'

    ADMIN_ROLE_NAME: str = 'admin'
    AUTHOR_ROLE_NAME: str = 'author'
    MODERATOR_ROLE_NAME: str = 'moderator'

    DB_TYPE: str
    DB_API: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_LIFESPAN: int
    AUTH_LOGIN_FIELD: str = 'email'  # залогин по email как дефолт

    APP_TITLE: str
    APP_DESCRIPTION: str
    APP_VERSION: str

    model_config = ConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def database_url(self) -> str:
        return (
            f'{self.DB_TYPE}+{self.DB_API}'
            f'://{self.DB_USER}:{self.DB_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )

    @property
    def alembic_database_url(self) -> str:
        return (
            f'{self.DB_TYPE}'
            f'://{self.DB_USER}:{self.DB_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


settings = Settings()
