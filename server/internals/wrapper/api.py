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


class API:
    """
    Handles managing API requests.
    """
    # Type hints
    __slots__ = ("config",)

    def __init__(
            self,
            config: APIConfig
    ) -> None:
        """
        Initializes the API class.

        Args:
            config (APIConfig): The configuration to use.
        """
