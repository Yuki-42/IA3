"""
Contains the Creator handler.
"""

# Standard Library Imports
from typing import List, Dict

# Third Party Imports

# Local Imports
from ..response import Response
from ..types import Creator
from ...config import API as APIConfig
from ...logging import SuppressedLoggerAdapter
from ...requester import Requester


class CreatorHandler:
    """
    Handles managing Creator requests.
    """

    __slots__ = ("config", "logger", "baseUrl", "requester")

    def __init__(
            self,
            config: APIConfig,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the CreatorHandler class.

        Args:
            config (APIConfig): The configuration to use.
        """
        self.baseUrl = f"{config.base}/creators"
        self.logger = logger
        self.requester = requester

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
        response: Dict = self.requester.get(self.baseUrl, {
            "page": page,
            "page_size": pageSize
        })

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
        self.logger.info(f"Getting creator details with id: {id}")
        return Creator(**self.requester.get(f"{self.baseUrl}/{id}"))
