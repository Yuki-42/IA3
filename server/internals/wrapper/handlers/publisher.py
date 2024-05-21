"""
Contains the Publisher handler.
"""

# Standard Library Imports
from typing import Dict, List

# Local Imports
from ..response import Response
from ..types import Publisher
from ...clogging import SuppressedLoggerAdapter
from ...requester import Requester


# Third Party Imports


class PublisherHandler:
    """
    Handles managing Publisher requests.
    """

    __slots__ = ("logger", "baseUrl", "requester")

    def __init__(
            self,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the PublisherHandler class.

        Args:
            logger (SuppressedLoggerAdapter): The logger to use.
            requester (Requester): The requester to use.
        """
        self.baseUrl = "publishers"
        self.logger = logger
        self.requester = requester

    def list(
            self,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of publishers.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.

        Returns:
            List[Publisher]: A list of publishers.
        """
        response: Dict = self.requester.get(
            self.baseUrl, {
                "page": page,
                "page_size": pageSize
            }
            )

        publishers: List[Publisher] = [
            Publisher(**publisher) for publisher in response["results"]
        ]

        return Response(
            data=response,
            results=publishers
        )

    def details(
            self,
            id: int | str
    ) -> Publisher:
        """
        Gets a publisher.

        Args:
            id (int | str): The id of the publisher (can be either rawgId or slug).

        Returns:
            Publisher: The publisher.
        """
        self.logger.info(f"Getting publisher details with id: {id}")
        return Publisher(**self.requester.get(f"{self.baseUrl}/{id}"))
