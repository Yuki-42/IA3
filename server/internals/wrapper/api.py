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
    __slots__ = (
        "config",
        "logger",
        "requester",
        "creator",
        "developer",
        "game",
    )

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
        self.logger = createLogger("API", level=config.logging.level, config=config)

        self.requester: Requester = Requester(config)  # Create a requester object to use

        # Create the handlers
        self.creator = CreatorHandler(self.logger, self.requester)
        self.developer = DeveloperHandler(self.logger, self.requester)
        self.game = GameHandler(self.logger, self.requester)
