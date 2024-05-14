"""
Contains classes representing config data.
"""
# Standard Library Imports
from logging import DEBUG, ERROR, INFO, WARNING
from os import environ

# Third Party Imports
from dotenv import load_dotenv as loadEnv


class Owner:
    """
    Contains owner related config data.
    """
    name: str
    contact: str

    def __init__(
            self
    ) -> None:
        """
        Initializes the Owner object.

        Returns:
            None
        """
        self.name = environ.get("SERVER_OWNER_NAME")
        self.contact = environ.get("SERVER_OWNER_CONTACT")


class SSL:
    """
    Contains SSL related config data.
    """
    cert: str
    key: str
    enabled: bool

    def __init__(
            self
    ) -> None:
        """
        Initializes the SSL object.

        Returns:
            None
        """
        self.cert = environ.get("SERVER_SSL_CERT")
        self.key = environ.get("SERVER_SSL_KEY")
        self.enabled = environ.get("SERVER_SSL_ENABLED") == "True"


class Server:
    """
    Contains server related config data.
    """
    host: str
    port: int
    debug: bool
    username: str
    password: str
    ssl: SSL
    owner: Owner

    def __init__(
            self
    ) -> None:
        """
        Initializes the Server object.

        Returns:
            None
        """
        self.host = environ.get("SERVER_HOST")
        self.port = int(environ.get("SERVER_PORT"))
        self.debug = environ.get("SERVER_DEBUG") == "True"
        self.username = environ.get("SERVER_USER")
        self.password = environ.get("SERVER_PASSWORD")
        self.defaultTheme = environ.get("SERVER_DEFAULT_THEME")
        self.ssl = SSL()
        self.owner = Owner()


class Logging:
    """
    Contains logging related config data.
    """
    level: int
    writeToFile: bool

    def __init__(
            self
    ) -> None:
        """
        Initializes the Logging object.

        Returns:
            None
        """
        self.writeToFile = environ.get("LOGGING_WRITE_TO_FILE") == "True"

        match environ.get("LOGGING_LEVEL").lower():
            case "info":
                self.level = INFO
            case "debug":
                self.level = DEBUG
            case "warning":
                self.level = WARNING
            case "error":
                self.level = ERROR
            case _:
                self.level = INFO


class API:
    """
    Contains API related config data.
    """
    key: str
    base: str

    def __init__(
            self
    ) -> None:
        """
        Initializes the API object.

        Returns:
            None
        """
        self.key = environ.get("API_KEY")
        self.base = environ.get("API_BASE")


class Config:
    """
    Contains config data.
    """
    server: Server
    logging: Logging
    api: API

    def __init__(
            self
    ) -> None:
        """
        Initializes the Data object.

        Returns:
            None
        """
        # Load environment variables
        loadEnv()

        self.server = Server()
        self.logging = Logging()
        self.api = API()
