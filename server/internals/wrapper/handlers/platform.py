"""
Contains the Platform handler.
"""

# Standard Library Imports
from typing import List, Dict

# Third Party Imports

# Local Imports
from ..response import Response
from ..types import Platform
from ...logging import SuppressedLoggerAdapter
from ...requester import Requester


class PlatformHandler:
    """
    Handles managing Platform requests.
    """

    __slots__ = ("logger", "baseUrl", "requester")

    def __init__(
            self,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the PlatformHandler class.

        Args:
            logger (SuppressedLoggerAdapter): The logger to use.
            requester (Requester): The requester to use.
        """
        self.baseUrl = "platforms"
        self.logger = logger
        self.requester = requester

    def list(
            self,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of platforms.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.

        Returns:
            List[Platform]: A list of platforms.
        """
        response: Dict = self.requester.get(self.baseUrl, {
            "page": page,
            "page_size": pageSize
        })

        platforms: List[Platform] = [
            Platform(**platform) for platform in response["results"]
        ]

        return Response(
            data=response,
            results=platforms
        )

    def details(
            self,
            id: int | str
    ) -> Platform:
        """
        Gets a platform.

        Args:
            id (int | str): The id of the platform (can be either rawgId or slug).

        Returns:
            Platform: The platform.
        """
        self.logger.info(f"Getting platform details with id: {id}")
        return Platform(**self.requester.get(f"{self.baseUrl}/{id}"))

    def parents(
            self,
            page: int = 1,
            pageSize: int = 20,
            ordering: str = None
    ) -> Response:
        """
        Gets a list of parent platforms.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.
            ordering (str): Which field to use when ordering the results.

        Returns:
            Response: A list of parent platforms.
        """
        response: Dict = self.requester.get(f"{self.baseUrl}/lists/parents", {
            "page": page,
            "page_size": pageSize
        })

        platforms: List[Platform] = [
            Platform(**platform) for platform in response["results"]
        ]

        return Response(
            data=response,
            results=platforms
        )
