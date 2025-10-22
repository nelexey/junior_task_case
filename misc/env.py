from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_FILENAME: str

    @property
    def database_url(self) -> str:
        return f"sqlite:///./{self.DB_FILENAME}"


settings = Settings(_env_file='.env') # type: ignore