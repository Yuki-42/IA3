"""
Contains the miscellaneous methods associated with the project but not part of the main logic of the system
"""
# Standard library imports
from logging import FileHandler, Formatter, Handler, INFO, Logger, LoggerAdapter, StreamHandler, getLogger, LogRecord
from os import getcwd, mkdir, path
from pathlib import Path
from sqlite3 import connect, Cursor
from sys import stdout
from threading import Lock
from typing import Literal, Type

# External imports
from flask import Request, has_request_context, request, Response, g

# Constants
databaseLock: Lock = Lock()


def getEscapeCode(
        baseColour: str,
        bold: bool = False,
        underline: bool = False,
) -> str:
    """
    Gets the ANSI escape code for the given colour.

    Args:
        baseColour (str): The base colour to get the ANSI escape code for.
        bold (bool): Whether the text should be bold.
        underline (bool): Whether the text should be underlined.

    Returns:
        str: The ANSI escape code for the given colour.

    Raises:
        ValueError: If the given colour is not a valid colour.

    Reference:
        https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
    """
    if baseColour.endswith("_H"):  # Specifies that the colour is of a high intensity. (Defined as 90-97)
        baseColour = baseColour[:-2]
        highIntensity: bool = True
    else:
        highIntensity = False

    match baseColour.upper():
        case "BLACK":
            colourCode = 30
        case "RED":
            colourCode = 31
        case "GREEN":
            colourCode = 32
        case "YELLOW":
            colourCode = 33
        case "BLUE":
            colourCode = 34
        case "PURPLE":
            colourCode = 35
        case "CYAN":
            colourCode = 36
        case "WHITE":
            colourCode = 37
        case _:
            raise ValueError(f"{baseColour} is not a valid colour.")

    if highIntensity:
        colourCode += 60

    if bold:
        formatter: str = "1;"
    elif underline:
        formatter = "4;"
    elif bold and underline:
        formatter = "1;4;"
    else:
        formatter = ""
    # Assemble the ANSI escape code
    return f"\033[{formatter}{colourCode}m"


class ColourCodedFormatter(Formatter):
    """
    A formatter that adds colour coding to the log messages.
    """
    # Type hints
    colourCoding: dict[str, str]

    def __init__(
            self,
            fmt: str | None = None,
            datefmt: str | None = None,
            style: Literal["%", "{", "$"] = "%",
            colourCoding: dict[str, str] = None
    ):
        super().__init__(fmt, datefmt, style)

        if colourCoding is None:
            colourCoding = {
                "DEBUG": getEscapeCode("CYAN"),
                "INFO": getEscapeCode("GREEN"),
                "WARNING": getEscapeCode("YELLOW"),
                "ERROR": getEscapeCode("RED"),
                "CRITICAL": getEscapeCode("RED_H"),
            }
        self.colourCoding = colourCoding

    def format(self, record: LogRecord) -> str:
        """
        Formats the log message.

        Args:
            record (LogRecord): The log record to format.

        Returns:
            str: The formatted log message.
        """

        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remoteAddress = request.remote_addr
            record.userAgent = request.user_agent
            record.cookies = request.cookies.__str__()

        else:
            record.url = None
            record.method = None
            record.remoteAddress = None
            record.userAgent = None
            record.cookies = None

        try:
            record.levelname = f"{self.colourCoding[record.levelname]}{record.levelname}\033[0m"
        except KeyError:  # Handles the case where the level name is not in the colour coding dictionary
            pass

        return super().format(record)


# TODO: Remove this if it is not used
class RequestFormatter(Formatter):
    """
    A formatter that adds colour coding to the log messages and includes the request information.
    """

    def __init__(
            self,
            fmt: str | None = None,
            datefmt: str | None = None,
            style: Literal["%", "{", "$"] = "%",
            colourCoding: dict[str, str] = None
    ):
        super().__init__(fmt, datefmt, style)

        if colourCoding is None:
            colourCoding = {
                "DEBUG": getEscapeCode("CYAN"),
                "INFO": getEscapeCode("GREEN"),
                "WARNING": getEscapeCode("YELLOW"),
                "ERROR": getEscapeCode("RED"),
                "CRITICAL": getEscapeCode("RED_H"),
            }
        self.colourCoding = colourCoding

    def format(self, record: LogRecord) -> str:
        """
        Formats the log message.

        Args:
            record (LogRecord): The log record to format.

        Returns:
            str: The formatted log message.
        """
        try:
            record.levelname = f"{self.colourCoding[record.levelname]}{record.levelname}\033[0m"
        except KeyError:
            pass
        return super().format(record)


class DatabaseLogHandler(Handler):
    """
    A handler that logs all information to a sqlite database and periodically removes logs older than one week.
    """
    __slots__ = ("file", "connection", "cursor")

    def __init__(
            self,
            file: Path | str = None
    ) -> None:
        """
        Initializes the handler.

        Args:
            file (Path | str): The file to log to.
        """
        if file is None:
            file = Path(f"{getcwd()}/Logs/logs.db")  # Default to the logs.db file in the Logs directory
        super().__init__()
        self.file = file
        self.connection = connect(
            file,
            check_same_thread=False
        )
        self.cursor: Cursor = self.connection.cursor()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                id VARCHAR(36) PRIMARY KEY,
                timestamp TEXT,
                level TEXT,
                message TEXT
            );
            """
        )
        # Check if the logs table exists
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weblogs (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                level TEXT,
                message TEXT,
                url TEXT,
                method TEXT,
                remote_address TEXT,
                user_agent TEXT,
                cookies TEXT,
                headers TEXT
            );
            """
        )
        # self.cursor.execute(
        #     """
        #     CREATE
        #     """
        # )

        # Close the cursor
        self.cursor.close()

    def emit(  # TODO: Convert this to use the request object, and e object to log the request information.
            self,
            record: LogRecord
    ) -> None:
        """
        Emits the log record to the sqlite database.

        Planning:
            Theoretically, this should have access to the request object, so it can log the request information.

        Args:
            record (LogRecord): The log record to emit.

        Returns:
            None
        """

    def logRequest(
            self,
            record: RequestLogRecord
    ) -> None:
        """
        Emits the log record to the sqlite database.

        Args:
            record (LogRecord): The log record to emit.
        """
        try:
            databaseLock.acquire()
            self.cursor.execute(
                """
                INSERT INTO logs (
                    timestamp,
                    level,
                    message,
                    url,
                    method,
                    remote_address,
                    user_agent,
                    cookies,
                    headers
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.created,
                    record.levelname,
                    record.getMessage(),
                    record.request.url,
                    record.request.method,
                    record.request.remote_addr,
                    record.request.user_agent.string,
                    record.request.cookies.__str__(),
                    record.request.headers.__str__()
                )
            )

            self.connection.commit()
        finally:
            databaseLock.release()

    def logResponse(
            self,
            record: RequestLogRecord
    ) -> None:
        """
        Emits the log record to the sqlite database.

        Args:
            record (LogRecord): The log record to emit.
        """
        try:
            databaseLock.acquire()
            self.cursor.execute(
                """
                INSERT INTO logs (
                    timestamp,
                    level,
                    message,
                    url,
                    method,
                    remote_address,
                    user_agent,
                    cookies,
                    headers
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.created,
                    record.levelname,
                    record.getMessage(),
                    record.request.url,
                    record.request.method,
                    record.request.remote_addr,
                    record.request.user_agent.string,
                    record.request.cookies.__str__(),
                    record.request.headers.__str__()
                )
            )

            self.connection.commit()
        finally:
            databaseLock.release()


# Custom LoggerAdapter that can be disabled
class SuppressedLoggerAdapter(LoggerAdapter):
    """
    A logger adapter that can be disabled.
    """
    # Type hints
    suppressed: bool

    def __init__(self, logger: Logger, extra: dict[str, str] | None = None):
        super().__init__(logger, extra)
        self.suppressed = False

    def __del__(self):
        """
        This method is called when the object is deleted.

        Returns:
            None
        """
        del self

    def suppress(self):
        """
        Suppresses the logger.
        """
        self.suppressed = True

    def unsuppress(self):
        """
        Unsuppresses the logger.
        """
        self.suppressed = False

    def log(self, level: int, msg: str, *args, **kwargs):
        """
        Logs the message to the logger.

        Args:
            level (int): The level of the log message.
            msg (str): The log message.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not self.suppressed:
            super().log(level, msg, *args, **kwargs)


class EndpointLoggerAdapter(LoggerAdapter):
    """
    A logger adapter that can be disabled.
    """
    # Type hints
    suppressed: bool

    def __init__(
            self,
            logger: Logger,
            extra: dict[str, str] | None = None
    ) -> None:
        """
        Initializes the logger adapter.

        Args:
            logger (Logger): The logger to adapt.
            extra (dict[str, str] | None):
        """
        super().__init__(logger, extra)
        self.suppressed = False

    def suppress(self) -> None:
        """
        Suppresses the logger.
        """
        self.suppressed = True

    def unsuppress(self) -> None:
        """
        Unsuppresses the logger.
        """
        self.suppressed = False

    def log(
            self,
            level: int,
            msg: str,
            *args,
            **kwargs
    ) -> None:
        """
        Logs the message to the logger.

        Args:
            level (int): The level of the log message.
            msg (str): The log message.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not self.suppressed:
            super().log(level, msg, *args, **kwargs)

    def logRequest(
            self,
            _request: Request
    ) -> None:
        """
        Logs the request to the endpoint.

        Args:
            _request (Request): The request to log.
        """
        headers: str = ""
        for key, value in request.headers:
            headers += f"{key}: {value}  "

        self.log(
            INFO,
            f"Request [{g.uuid}] from {request.remote_addr} to {request.path} with method {request.method} from user agent {request.user_agent} with cookies {request.cookies}"
        )
        if self.logger.hasHandlers():
            # Get the index of the handler
            for index, handler in enumerate(self.logger.handlers):
                if isinstance(handler, DatabaseLogHandler):
                    handler.logRequest(
                        RequestLogRecord(
                            _request=_request,
                            record=self.logger.makeRecord(
                                self.logger.name,
                                INFO,
                                "",
                                0,
                                f"Request from {request.remote_addr} to {request.path} with method {request.method} "
                                f"and headers {headers} from user agent {request.user_agent}",
                                (),
                                None,
                                "",
                                ""
                            )
                        )
                    )
                    break

    def logResponse(
            self,
            _request: Request
    ) -> None:
        """
        Logs the response to the endpoint.

        Args:
            _request (Request): The request to log.
        """
        headers: str = ""
        for key, value in request.headers:
            headers += f"{key}: {value}  "

        self.log(
            INFO,
            f"Response from {request.remote_addr} to {request.path} with method {request.method} from user agent {request.user_agent} with cookies {request.cookies}"
        )
        if self.logger.hasHandlers():
            # Get the index of the handler
            for index, handler in enumerate(self.logger.handlers):
                if isinstance(handler, DatabaseLogHandler):
                    handler.dbEmit(
                        RequestLogRecord(
                            request=_request,
                            name=self.logger.name,
                            level=INFO,
                            pathname="",
                            lineno=0,
                            msg=f"Response from {request.remote_addr} to {request.path} with method {request.method} "
                                f"and headers {headers} from user agent {request.user_agent}",
                            args=(),
                            exc_info=None,
                            func="",
                            sinfo=""
                        )
                    )
                    break


def createLogger(
        name: str,
        level: int = INFO,
        formatString: str = "[%(asctime)s] [%(loggername)s] [%(levelname)s] %(message)s",
        handlers: list[Handler] = None,
        doColour: bool = True,
        colourCoding: dict[str, str] = None,
        adapterMode: Type[SuppressedLoggerAdapter] | Type[EndpointLoggerAdapter] = SuppressedLoggerAdapter,
        dbFile: Path | str = Path(f"{getcwd()}/Logs/logs.db")
) -> SuppressedLoggerAdapter | EndpointLoggerAdapter:
    """
    Creates a logger with the specified name, logging path, level, and formatter.

    Args:
        name (str): The name of the logger.
        level (str): The level of the logger.
        formatString (str): The format string for the logger.
        handlers (list): Additional handlers for the logger.
        doColour (bool): Whether to use colour coding in the logger for logging outputs.
        colourCoding (dict): The colour coding for the logger. Defaults to the default colour coding defined in the
            function.
        adapterMode (str): The mode of the adapter. Can be either SuppressedLoggerAdapter or EndpointLoggerAdapter.
        dbFile (Path | str): The file to log to.

    Returns:
        logger (Logger): The logger object.

    """
    if not path.exists(Path(f"{getcwd()}/Logs/")):
        mkdir(Path(f"{getcwd()}/Logs/"))

    loggingDirectory: str = name
    logFileName: str = name + "_"

    # Check if the logging directory exists, if not, create it
    if not path.exists(Path(f"{getcwd()}/Logs/{loggingDirectory}")):
        mkdir(Path(f"{getcwd()}/Logs/{loggingDirectory}"))

    logger: Logger = getLogger(name)  # Sets the logger's name
    logger.setLevel(level)  # Sets the logger's level

    if logger.hasHandlers():  # This checks if the logger has already been created and if it has, it replaces the
        # handlers with the new ones
        logger.handlers.clear()

    if handlers is None:
        handlers: list[Handler] = [
            FileHandler(
                Path(
                    f"{getcwd()}/Logs/{loggingDirectory}/{logFileName}.log"
                ),
                encoding="utf-8",
            ),
            StreamHandler(
                stdout
            )
        ]

    colourFormatter: ColourCodedFormatter = ColourCodedFormatter(formatString, colourCoding=colourCoding)
    formatter: Formatter = Formatter(formatString)

    if adapterMode == EndpointLoggerAdapter:
        handlers.append(DatabaseLogHandler())

    for handler in handlers:
        if not doColour or isinstance(handler, FileHandler):
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            pass
        else:
            handler.setFormatter(colourFormatter)
            logger.addHandler(handler)

    # This works for some reason
    # noinspection PyUnresolvedReferences
    return adapterMode(logger, extra={"loggername": name})
