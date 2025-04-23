from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_USER: str = "kernreaktor_experte"
    MYSQL_PASSWORD: str = "kernreaktor"
    MYSQL_ROOT_PASSWORD: str = "root"
    MYSQL_DATABASE: str = "kernreaktor"
    DB_HOST: str = "127.0.0.2"
    DB_PORT: int = 3306

    DEBUG: bool = False
    API_PORT: int = 52345

    @property
    def sqlalchemy_database_url(self) -> str:
        """Build the SQLAlchemy-compatible database URL from env vars"""
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.MYSQL_DATABASE}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
