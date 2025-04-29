from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Settings class for the application.
    This class uses Pydantic to manage application settings and environment variables.
    It provides a convenient way to access and validate configuration values.

    Attributes:
    MYSQL_USER (str): MySQL username.
    MYSQL_PASSWORD (str): MySQL password.
    MYSQL_ROOT_PASSWORD (str): MySQL root password.
    MYSQL_DATABASE (str): MySQL database name.
    DB_HOST (str): Database host.
    DB_PORT (int): Database port. Default is 3306.
    SECRET_KEY (str): Secret key for the application. Generate with openssl rand -hex 32
    DEBUG (bool): Debug mode. Default is True. This should be set to False in production, since it drops the database with every restart.
    API_PORT (int): Port for the API. Default is 52345.
    DOCKER (bool): Flag to indicate if the application is running in a Docker container. Default is False.
    PVE_TOKEN_ID (str): Proxmox VE token ID. You can create a token in the Proxmox web interface under Datacenter -> Permissions -> API Tokens.
    PVE_API_SECRET (str): Proxmox VE API secret. You can create a token in the Proxmox web interface under Datacenter -> Permissions -> API Tokens.
    MQTT_BROKER (str): MQTT broker address. For stability in testing use the dockerised MQTT broker. Using test.mosquitto.org for testing is not recommended, since many users are using it and its not guaranteed that the broker is available or used by someone else.
    MQTT_PORT (int): MQTT broker port. Default is 1883.
    MQTT_API_USER (str | None): MQTT API username. Default is None. Later in production this should be set to a user with limited permissions.
    MQTT_API_PASSWORD (str | None): MQTT API password. Default is None. Later in production this should be set to a user with limited permissions.

    """

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
    PVE_TOKEN_ID: str = "root@pam!UUID"
    PVE_API_SECRET: str = "d6731b0f-e316-49fa-8a08-b158d21b760a"
    MQTT_BROKER: str = "127.0.0.1"
    MQTT_PORT: int = 1883
    MQTT_API_USER: str | None = None
    MQTT_API_PASSWORD: str | None = None

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
