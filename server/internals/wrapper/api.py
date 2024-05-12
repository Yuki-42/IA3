"""
Contains the API class.
"""

# Standard Library Imports

# Third Party Imports

# Local Imports
from .handlers import *
from ..config import Config
from ..logging import createLogger
from ..requester import Requester


class API:
    """
    Handles managing API requests.
    """
    # Type hints
    __slots__ = ("config", "logger", "requester", "creator", "developer")

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

        self.requester: Requester = Requester(config)  # Create a requester object to use
        self.creator = CreatorHandler(self.logger, self.requester)
        self.developer = DeveloperHandler(self.logger, self.requester)
