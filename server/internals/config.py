"""
Configuration module for the server.
"""
# Standard Library Imports
from secrets import token_urlsafe as tokenUrlsafe
from socket import gethostbyname, gethostname

# Third Party Imports
from dynaconf import Dynaconf

# Load the settings object
settings: Dynaconf = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["config.yaml"],
    load_dotenv=True,
    environments=True,
    env_switcher="DYNACONF_ENV",
    lowercase_read=True
)


# Create a class to consume the settings object

class Config:
    """
    Adapter and logic processing class for the settings object.
    """

    def __init__(self):
        """
        Initializes the Config object.
        """
        self.server = self.server()
        self.logging = self.logging()

    class server:
        """
        Contains server related config data.
        """
        __slots__ = [
            "host",
            "port",
            "debug",
            "secretKey"
        ]

        def __init__(self):
            """
            Initializes the server object.
            """
            self.host: str = settings.server.host if settings.server.host != "auto" else gethostbyname(gethostname())
            self.port: int = settings.server.port
            self.debug: bool = settings.server.debug == "True"
            self.secretKey: str = settings.server.secretKey if settings.server.secretKey != "auto" else tokenUrlsafe(32)

        class owner:
            """
            Contains owner related config data.
            """
            __slots__ = [
                "name",
                "contact"
            ]

            def __init__(self):
                """
                Initializes the owner object.
                """
                self.name: str = settings.server.owner.name
                self.contact: str = settings.server.owner.contact

        class auth:
            """
            Contains auth related config data.
            """
            __slots__ = [
                "username",
                "password"
            ]

            def __init__(self):
                """
                Initializes the auth object.
                """
                username: str = settings.server.auth.username
                password: str = settings.server.auth.password

                # If the any of the values are "auto", generate a 16 digit random string
                if username == "auto":
                    username = tokenUrlsafe(6)
                if password == "auto":
                    password = tokenUrlsafe(16)

                self.username = username
                self.password = password

        class ssl:
            """
            Contains SSL related config data.
            """
            __slots__ = [
                "cert",
                "key",
                "enabled",
            ]

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
    publicHost: str
    serverLocal: str
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
        self.publicHost = environ.get("SERVER_PUBLIC_HOST")
        self.debug = environ.get("SERVER_DEBUG") == "True"
        self.username = environ.get("SERVER_USER")
        self.password = environ.get("SERVER_PASSWORD")
        self.defaultTheme = environ.get("SERVER_DEFAULT_THEME")
        self.serverLocal = environ.get("SERVER_LOCAL") if environ.get("SERVER_LOCAL") else "localhost"
        self.ssl = SSL()
        self.owner = Owner()


    class logging:
        """
        Contains logging related config data.
        """

        def __init__(self):
            """
            Initializes the logging object.
            """
            self.level: int = settings.logging.level
            self.handlers: list[str] = settings.logging.handlers
            self.db = self.db() if "db" in settings.logging.handlers else None

        class db:
            """
            Contains logging database related config information.
            """
            __slots__ = [
                "host",
                "port",
                "username",
                "password",
                "database"
            ]

            def __init__(self):
                """
                Initializes the db object.
                """
                self.host: str = settings.logging.db.host
                self.port: int = settings.logging.db.port
                self.username: str = settings.logging.db.username
                self.password: str = settings.logging.db.password
                self.database: str = settings.logging.db.database

    class api:
        """
        Contains API related config data.
        """

        def __init__(self):
            """
            Initializes the API object.
            """
            self.host: str = settings.api.host
            self.port: int = settings.api.port
            self.ssl: bool = settings.api.ssl == "True"
            self.secretKey: str = settings.api.secretKey if settings.api.secretKey != "auto" else tokenUrlsafe(32)
            self.auth = self.auth()

        class auth:
            """
            Contains auth related config data.
            """
            __slots__ = [
                "username",
                "password"
            ]

            def __init__(self):
                """
                Initializes the auth object.
                """
                username: str = settings.api.auth.username
                password: str = settings.api.auth.password
