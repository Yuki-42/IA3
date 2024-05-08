"""
Contains the base handler.
"""

# Standard Library Imports
from typing import List, Dict

# Third Party Imports
from requests import get, Response

# Local Imports
from ...config import API as APIConfig
from ...logging import SuppressedLoggerAdapter


class BaseHandler:
    """
    Handles managing base requests.
    """
    __slots__ = ("config", "logger", "baseUrl")

    def __init__(
            self,
            config: APIConfig,
            logger: SuppressedLoggerAdapter
    ) -> None:
        """
        Initializes the BaseHandler class.

        Args:
            config (APIConfig): The configuration to use.
        """
        self.config = config
        self.logger = logger
        self.baseUrl = f"{config.base}/base"

    async def get(
            self,
            url: str,
            params: Dict = None
    ) -> Dict:
        """
        Gets a response from the api.

        Returns:
            List[Dict]: The response from the api.
        """
        # Handle params
        if params is None:
            params = {}

        params["key"] = self.config.key  # Add the api key

        response: Response = get(
            url,
            params=params,
        )

        response.raise_for_status()
        return response.json()
