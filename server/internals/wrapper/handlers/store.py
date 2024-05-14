"""
Contains the Store handler.
"""

# Standard Library Imports
from typing import Dict, List

# Local Imports
from ..response import Response
from ..types import Store
from ...logging import SuppressedLoggerAdapter
from ...requester import Requester


# Third Party Imports


class StoreHandler:
    """
    Handles managing Store requests.
    """

    __slots__ = ("logger", "baseUrl", "requester")

    def __init__(
            self,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the StoreHandler class.

        Args:
            logger (SuppressedLoggerAdapter): The logger to use.
            requester (Requester): The requester to use.
        """
        self.baseUrl = "stores"
        self.logger = logger
        self.requester = requester

    def list(
            self,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of stores.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.

        Returns:
            List[Store]: A list of stores.
        """
        response: Dict = self.requester.get(
            self.baseUrl, {
                "page": page,
                "page_size": pageSize
            }
            )

        stores: List[Store] = [
            Store(**store) for store in response["results"]
        ]

        return Response(
            data=response,
            results=stores
        )

    def details(
            self,
            id: int | str
    ) -> Store:
        """
        Gets a store.

        Args:
            id (int | str): The id of the store (can be either rawgId or slug).

        Returns:
            Store: The store.
        """
        self.logger.info(f"Getting store details with id: {id}")
        return Store(**self.requester.get(f"{self.baseUrl}/{id}"))
