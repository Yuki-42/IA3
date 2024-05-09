"""
Contains classes representing config data.
"""
# Standard Library Imports
from os import environ
from logging import INFO, DEBUG, WARNING, ERROR

# Third Party Imports
from dotenv import load_dotenv as loadEnv


class Server:
    """
    Contains server related config data.
    """
    host: str
    port: int
    debug: bool
    password: str
    cert: str
    key: str
    ssl: bool

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
        self.password = environ.get("SERVER_PASSWORD")
        self.cert = environ.get("SERVER_CERT")
        self.key = environ.get("SERVER_KEY")
        self.ssl = environ.get("SERVER_SSL") == "True"


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
