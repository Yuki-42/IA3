"""
Funcs module.
"""
# Standard Library Imports
from logging import INFO, Handler, getLogger, Logger, FileHandler, StreamHandler, Formatter
from os import mkdir, path, getcwd
from pathlib import Path
from sys import stdout

# Local Imports
from . import SuppressedLoggerAdapter
from .formatters import ColourCodedFormatter
from .handlers import DatabaseLogHandler


def createLogger(
        name: str,
        level: int = INFO,
        formatString: str = "[%(asctime)s] [%(loggername)s] [%(levelname)s] %(message)s",
        handlers: list[Handler] = None,
        doColour: bool = True,
        colourCoding: dict[str, str] = None,
        doDb: bool = True,
        includeRequest: bool = False,
        dbFile: Path | str = Path(f"{getcwd()}/Logs/logs.db")
) -> SuppressedLoggerAdapter:
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
        doDb (bool): Whether to log to a database.
        includeRequest (bool): Whether to include the request information in the log.
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

    if doDb:
        handlers.append(DatabaseLogHandler(dbFile))

    for handler in handlers:
        if not doColour or isinstance(handler, FileHandler):
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            pass
        else:
            handler.setFormatter(colourFormatter)
            logger.addHandler(handler)

    # This works for some reason
    return SuppressedLoggerAdapter(logger, extra={"loggername": name})
