"""
Contains the API class.
"""

# Standard Library Imports
from typing import List, Optional

# Third Party Imports
from requests import get

# Local Imports
from .types import *
from .handlers import *
from ..config import Config, API as APIConfig
from ..logging import SuppressedLoggerAdapter, createLogger


class API:
    """
    Handles managing API requests.
    """
    # Type hints
    __slots__ = ("config", "logger", "creator")

    def __init__(
            self,
            config: Config
    ) -> None:
        """
        Initializes the API class.

        Args:
            config (Config): The configuration to use.
        """
        self.config = config.api
        self.logger = createLogger("API", level=config.logging.level)
        self.creator = CreatorHandler(config.api, self.logger)
