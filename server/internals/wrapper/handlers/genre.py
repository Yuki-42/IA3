"""
Contains the Genre handler.
"""

# Standard Library Imports
from typing import Dict, List

# Local Imports
from ..response import Response
from ..types import Genre
from ...clogging import SuppressedLoggerAdapter
from ...requester import Requester


# Third Party Imports


class GenreHandler:
    """
    Handles managing Genre requests.
    """

    __slots__ = ("logger", "baseUrl", "requester")

    def __init__(
            self,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the GenreHandler class.

        Args:
            logger (SuppressedLoggerAdapter): The logger to use.
            requester (Requester): The requester to use.
        """
        self.baseUrl = "genres"
        self.logger = logger
        self.requester = requester

    def list(
            self,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of genres.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.

        Returns:
            List[Genre]: A list of genres.
        """
        response: Dict = self.requester.get(
            self.baseUrl, {
                "page": page,
                "page_size": pageSize
            }
            )

        genres: List[Genre] = [
            Genre(**genre) for genre in response["results"]
        ]

        return Response(
            data=response,
            results=genres
        )

    def details(
            self,
            id: int | str
    ) -> Genre:
        """
        Gets a genre.

        Args:
            id (int | str): The id of the genre (can be either rawgId or slug).

        Returns:
            Genre: The genre.
        """
        self.logger.info(f"Getting genre details with id: {id}")
        return Genre(**self.requester.get(f"{self.baseUrl}/{id}"))
