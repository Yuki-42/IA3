"""
Contains the content filter class for the project
"""
# External imports
from json import JSONDecodeError, dump, load

# Internal imports
from .logging import createLogger, SuppressedLoggerAdapter
from .databaseold import Database


def escapeMessage(message: str) -> str:
    """
    Escapes a message by replacing html characters with their escaped counterparts.

    Args:
        message (str): The message to be escaped.

    Returns:
        str: The escaped message.
    """
    return (
        message
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
        .replace("'", "&#039;")
    )


class ContentFilter:
    """
    This class is responsible for handling all automated content moderation.
    """

    # Type hints
    logger: SuppressedLoggerAdapter
    database: Database

    def __init__(self, database: Database):
        """
        This class is responsible for handling all automated content moderation.

        Returns:
            ContentFilter: The ContentFilter object.
        """
        self.logger = createLogger("ContentFilter")
        self.database = database
        self.logger.info("ContentFilter initialized")

    def checkMessage(self, message: str) -> bool:
        """
        Checks a message for banned words.

        Args:
            message (str): The message to be checked.

        Returns:
            bool: True if the message contains a banned word, False otherwise.
        """
        # This could probably be optimised using list interpretation
        for word in self.database.bannedWords:  # This can be optimised using any()
            if word.word in message:
                return True
        return False

    def censorMessage(self, message: str) -> str:
        """
        Censors a message by replacing banned words with asterisks.

        Args:
            message (str): The message to be censored.

        Returns:
            str: The censored message.
        """
        for word in self.database.bannedWords:
            message = message.replace(word.word, "*" * len(word.word))

        return message
