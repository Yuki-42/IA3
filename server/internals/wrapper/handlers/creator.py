"""
Contains the Creator handler.
"""

# Standard Library Imports
from typing import Dict, List

# Local Imports
from ..response import Response
from ..types import Creator
from ...logging import SuppressedLoggerAdapter
from ...requester import Requester


# Third Party Imports


class CreatorHandler:
    """
    Handles managing Creator requests.
    """

    __slots__ = ("logger", "baseUrl", "requester")

    def __init__(
            self,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the CreatorHandler class.

        Args:
            logger (SuppressedLoggerAdapter): The logger to use.
            requester (Requester): The requester to use.
        """
        self.baseUrl = "creators"
        self.logger = logger
        self.requester = requester

    def list(
            self,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of creators.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.

        Returns:
            List[Creator]: A list of creators.
        """
        response: Dict = self.requester.get(
            self.baseUrl, {
                "page": page,
                "page_size": pageSize
            }
            )

        creators: List[Creator] = [
            Creator(**creator) for creator in response["results"]
        ]

        return Response(
            data=response,
            results=creators
        )

    def details(
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
