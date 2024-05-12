"""
Contains the Creator handler.
"""

# Standard Library Imports
from typing import List, Dict

# Third Party Imports

# Local Imports
from ..response import Response
from ..types import Developer
from ...logging import SuppressedLoggerAdapter
from ...requester import Requester


class DeveloperHandler:
    """
    Handles managing Developer requests.
    """

    __slots__ = ("logger", "baseUrl", "requester")

    def __init__(
            self,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the DeveloperHandler class.

        Args:
            logger (SuppressedLoggerAdapter): The logger to use.
            requester (Requester): The requester to use.
        """
        self.baseUrl = "developers"
        self.logger = logger
        self.requester = requester

    def list(
            self,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of developers.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.

        Returns:
            List[Developer]: A list of developers.
        """
        response: Dict = self.requester.get(self.baseUrl, {
            "page": page,
            "page_size": pageSize
        })

        developers: List[Developer] = [
            Developer(**developer) for developer in response["results"]
        ]

        return Response(
            data=response,
            results=developers
        )

    def details(
            self,
            id: int | str
    ) -> Developer:
        """
        Gets a developer.

        Args:
            id (int | str): The id of the developer (can be either rawgId or slug).

        Returns:
            Developer: The developer.
        """
        self.logger.info(f"Getting developer details with id: {id}")
        return Developer(**self.requester.get(f"{self.baseUrl}/{id}"))
