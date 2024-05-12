"""
Contains the Tag handler.
"""

# Standard Library Imports
from typing import List, Dict

# Third Party Imports

# Local Imports
from ..response import Response
from ..types import Tag
from ...logging import SuppressedLoggerAdapter
from ...requester import Requester


class TagHandler:
    """
    Handles managing Tag requests.
    """

    __slots__ = ("logger", "baseUrl", "requester")

    def __init__(
            self,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the TagHandler class.

        Args:
            logger (SuppressedLoggerAdapter): The logger to use.
            requester (Requester): The requester to use.
        """
        self.baseUrl = "tags"
        self.logger = logger
        self.requester = requester

    def list(
            self,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of tags.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.

        Returns:
            List[Tag]: A list of tags.
        """
        response: Dict = self.requester.get(self.baseUrl, {
            "page": page,
            "page_size": pageSize
        })

        tags: List[Tag] = [
            Tag(**tag) for tag in response["results"]
        ]

        return Response(
            data=response,
            results=tags
        )

    def details(
            self,
            id: int | str
    ) -> Tag:
        """
        Gets a tag.

        Args:
            id (int | str): The id of the tag (can be either rawgId or slug).

        Returns:
            Tag: The tag.
        """
        self.logger.info(f"Getting tag details with id: {id}")
        return Tag(**self.requester.get(f"{self.baseUrl}/{id}"))
