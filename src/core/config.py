from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_TYPE: str
    DB_API: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    APP_TITLE: str
    APP_DESCRIPTION: str

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
