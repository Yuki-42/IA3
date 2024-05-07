"""
Contains classes representing config data.
"""


class Server:
    """
    Contains server related config data.
    """
    host: str
    port: int
    debug: bool


class Logging:
    """
    Contains logging related config data.
    """
    level: str
    writeToFile: bool


class Data:
    """
    Contains config data.
    """
    server: Server
    logging: Logging

    def __init__(self, env: str) -> None:
        """
        Initializes the Data object.

        Args:
            env (str): The environment to use.
        """
        self.server = Server()
        self.logging = Logging()

        if env == "dev":
            self.server.host = "
