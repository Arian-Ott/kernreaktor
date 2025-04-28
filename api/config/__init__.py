from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    MYSQL_USER: str = "reaktor"
    MYSQL_PASSWORD: str = "reaktor"
    MYSQL_ROOT_PASSWORD: str = "root"
    MYSQL_DATABASE: str = "reaktor"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    SECRET_KEY: str = "your_secret_key"
    DEBUG: bool = True
    API_PORT: int = 52345
    DOCKER: bool = False
    PVE_TOKEN_ID: str  = "root@pam!UUID" 
    PVE_API_SECRET: str = "d6731b0f-e316-49fa-8a08-b158d21b760a"
    MQTT_BROKER:str = "127.0.0.1"  
    MQTT_PORT:int = 1883
    MQTT_API_USER:str | None = None
    MQTT_API_PASSWORD:str | None = None

    @property
    def sqlalchemy_database_url(self) -> str:
        """Build the SQLAlchemy-compatible database URL from env vars"""
        if not self.DEBUG and self.DOCKER:
            self.DB_HOST = "maria"
            self.MQTT_BROKER = "reaktor-mqtt"
            
            
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.MYSQL_DATABASE}"
        )

    class Config:
        env_file = Path(__file__).parent.parent.parent / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
