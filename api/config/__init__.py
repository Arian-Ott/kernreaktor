from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_USER: str = "reaktor"
    MYSQL_PASSWORD: str = "reaktor"
    MYSQL_ROOT_PASSWORD: str = "root"
    MYSQL_DATABASE: str = "reaktor"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    SECRET_KEY: str = "your_secret_key"
    DEBUG: bool = False
    API_PORT: int = 52345
    DOCKER: bool = False

    @property
    def sqlalchemy_database_url(self) -> str:
        """Build the SQLAlchemy-compatible database URL from env vars"""
        if not self.DEBUG and self.DOCKER:
            self.DB_HOST = "maria"
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.MYSQL_DATABASE}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
