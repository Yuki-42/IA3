"""
Contains classes representing config data.
"""
# Standard Library Imports
from os import environ

# Third Party Imports
from dotenv import load_dotenv as loadEnv


class Server:
    """
    Contains server related config data.
    """
    host: str
    port: int
    debug: bool

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


class Logging:
    """
    Contains logging related config data.
    """
    level: str
    writeToFile: bool

    def __init__(
            self
    ) -> None:
        """
        Initializes the Logging object.

        Returns:
            None
        """
        self.level = environ.get("LOGGING_LEVEL")
        self.writeToFile = environ.get("LOGGING_WRITE_TO_FILE") == "True"


class Config:
    """
    Contains config data.
    """
    server: Server
    logging: Logging

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
