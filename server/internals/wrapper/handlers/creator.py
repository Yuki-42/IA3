"""
Contains the Creator handler.
"""

# Standard Library Imports
from typing import List, Dict

# Third Party Imports
from requests import get

# Local Imports
from .base import BaseHandler
from ..types import Creator
from ..response import Response
from ...config import API as APIConfig
from ...logging import SuppressedLoggerAdapter


class CreatorHandler(BaseHandler):
    """
    Handles managing Creator requests.
    """
    def __init__(
            self,
            config: APIConfig,
            logger: SuppressedLoggerAdapter
    ) -> None:
        """
        Initializes the CreatorHandler class.

        Args:
            config (APIConfig): The configuration to use.
        """
        super().__init__(config, logger)
        self.baseUrl = f"{config.base}/creators"

    def getCreators(
            self,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of creators.

        Returns:
            List[Creator]: A list of creators.
        """
        response: Dict = self.get(self.baseUrl)

        creators: List[Creator] = [
            Creator(**creator) for creator in response["results"]
        ]

        return Response(
            data=response,
            results=creators
        )

    def getCreator(
            self,
            id: int | str
    ) -> Creator:
        """
        Gets a creator.

        Args:
            id (int | str): The id of the creator (can be either rawgId or slug).

        Returns:
            Creator: The creator.
        """
        response: Dict = self.get(f"{self.baseUrl}/{id}")

        return Creator(**response)
