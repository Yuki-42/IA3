"""
Contains the Creator handler.
"""

# Standard Library Imports
from typing import List, Dict
from datetime import datetime as Datetime

# Third Party Imports

# Local Imports
from ..response import Response
from ..types import Game, Platform, Store, Developer, Publisher, Genre, Tag
from ...helpers import addParameters
from ...logging import SuppressedLoggerAdapter
from ...requester import Requester


class GameHandler:
    """
    Handles managing Game requests.
    """

    __slots__ = ("logger", "baseUrl", "requester")

    def __init__(
            self,
            logger: SuppressedLoggerAdapter,
            requester: Requester
    ) -> None:
        """
        Initializes the GameHandler class.

        Args:
            logger (SuppressedLoggerAdapter): The logger to use.
            requester (Requester): The requester to use.
        """
        self.baseUrl = "games"
        self.logger = logger
        self.requester = requester

    def list(
            self,
            page: int = 1,
            pageSize: int = 20,
            search: str = None,
            searchPrecise: bool = None,
            searchExact: bool = None,
            parentPlatforms: List[int | Platform] = None,
            platforms: List[int | Platform] = None,
            stores: List[int | Store] = None,
            developers: List[int | str | Developer] = None,
            publishers: List[int | str | Publisher] = None,
            genres: List[int | str | Genre] = None,
            tags: List[int | str | Tag] = None,
            creators: List[int | str] = None,
            dates: List[str] = None,
            updated: str = None,
            platformsCount: int = None,
            metacritic: List[int] = None,
            excludeCollection: int = None,
            excludeAdditions: bool = None,
            excludeParents: bool = None,
            excludeGameSeries: bool = None,
            excludeStores: List[int] = None,
            ordering: str = None
    ) -> Response:
        """
        Gets a list of games.

        Args:
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.
            search (str): Search query.
            searchPrecise (bool): Disable fuzziness for the search query.
            searchExact (bool): Mark the search query as exact.
            parentPlatforms (List[int | Platform]): Filter by parent platforms, for example: [1, 2, 3].
            platforms (List[int | Platform]): Filter by platforms, for example: [4, 5].
            stores (List[int | Store]): Filter by stores, for example: [5, 6].
            developers (List[int | str | Developer]): Filter by developers, for example: [1612, 18893] or [valve-software, feral-interactive].
            publishers (List[int | str | Publisher]): Filter by publishers, for example: [354, 20987] or [electronic-arts, microsoft-studios].
            genres (List[int | str | Genre]): Filter by genres, for example: [4, 51] or [action, indie].
            tags (List[int | str | Tag]): Filter by tags, for example: [31, 7] or [singleplayer, multiplayer].
            creators (List[int | str | Creator]): Filter by creators, for example: [78, 28] or [cris-velasco, mike-morasky].
            dates (List[str | Datetime]): Filter by a release date, for example: [2010-01-01, 2018-12-31.1960-01-01, 1969-12-31].
            updated (str | Datetime): Filter by an update date, for example: 2020-12-01,2020-12-31.
            platformsCount (int): Filter by platforms count, for example: 1.
            metacritic (str): Filter by a metacritic rating, for example: [80, 100].
            excludeCollection (int): Exclude games from a particular collection, for example: 123.
            excludeAdditions (bool): Exclude additions.
            excludeParents (bool): Exclude games which have additions.
            excludeGameSeries (bool): Exclude games which included in a game series.
            excludeStores (List[int]): Exclude stores, for example: [5, 6].
            ordering (str): Available fields: name, released, added, created, updated, rating, metacritic. You can reverse the sort order adding a hyphen, for example: -released.

        Returns:
            List[Game]: A list of games.
        """
        # Create parameters dictionary
        parameters: Dict = {
            "page": page,
            "page_size": pageSize
        }

        # Add parameters
        parameters = addParameters(parameters, {  # This is almost definitely going to throw an error
            "search": search,
            "search_precise": searchPrecise,
            "search_exact": searchExact,
            "parent_platforms": parentPlatforms,
            "platforms": platforms,
            "stores": stores,
            "developers": developers,
            "publishers": publishers,
            "genres": genres,
            "tags": tags,
            "creators": creators,
            "dates": dates,
            "updated": updated,
            "platforms_count": platformsCount,
            "metacritic": metacritic,
            "exclude_collection": excludeCollection,
            "exclude_additions": excludeAdditions,
            "exclude_parents": excludeParents,
            "exclude_game_series": excludeGameSeries,
            "exclude_stores": excludeStores,
            "ordering": ordering
        })

        response: Dict = self.requester.get(
            self.baseUrl,
            parameters
        )

        games: List[Game] = [
            Game(**game) for game in response["results"]
        ]

        return Response(
            data=response,
            results=games
        )

    def dlcs(
            self,
            id: int | str,
            page: int = 1,
            pageSize: int = 20
    ) -> Response:
        """
        Gets a list of downloadable content (DLCs) for a game.

        Args:
            id (int | str): The id of the game (can be either rawgId or slug).
            page (int): A page number within the paginated result set.
            pageSize (int): Number of results to return per page.

        Returns:
            List[Game]: A list of games.
        """
        response: Dict = self.requester.get(
            f"{self.baseUrl}/{id}/additions",
            {
                "game_pk": id,
                "page": page,
                "page_size": pageSize
            }
        )

        games: List[Game] = [
            Game(**game) for game in response["results"]
        ]

        return Response(
            data=response,
            results=games
        )

    def details(
            self,
            id: int | str
    ) -> Game:
        """
        Gets a game.

        Args:
            id (int | str): The id of the game (can be either rawgId or slug).

        Returns:
            Game: The game.
        """
        self.logger.info(f"Getting game details with id: {id}")
        return Game(**self.requester.get(f"{self.baseUrl}/{id}"))