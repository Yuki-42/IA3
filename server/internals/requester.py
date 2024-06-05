"""
Contains the Requester class.
"""

# Standard Library Imports
from typing import Any, Callable, Dict, Optional
from uuid import uuid4

from flask import has_request_context
# Third Party Imports
from requests import Response, delete, get, post, put

# Internal Imports
from .config import Config
from .clogging import createLogger


class Requester:
    """
    Handles making requests to the RAWG API.
    """
    __sockets__ = ("config", "logger")

    def __init__(
            self,
            config: Config
    ) -> None:
        """
        Initializes the Requester object.

        Args:
            config (Config): The configuration object.
        """
        self.config = config
        self.logger = createLogger("Requester", level=config.logging.level, config=config, includeRequest=False)

    def get(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            overwriteUrl: bool = False,
            **kwargs
    ) -> Any:
        """
        Makes a GET request to the RAWG API.

        Args:
            url (str): The URL to make the request to.
            params (Optional[Dict[str, Any]]): The parameters to pass to the request.
            headers (Optional[Dict[str, str]]): The headers to pass to the request.
            overwriteUrl (bool): Whether to overwrite the whole url or not.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        return self._action(
            method=get,
            url=url,
            params=params,
            overwriteUrl=overwriteUrl,
            headers=headers,
            **kwargs
        )

    def post(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            overwriteUrl: bool = False,
            **kwargs
    ) -> Any:
        """
        Makes a POST request to the RAWG API.

        Args:
            url (str): The URL to make the request to.
            data (Optional[Dict[str, Any]]): The data to pass to the request.
            headers (Optional[Dict[str, str]]): The headers to pass to the request.
            overwriteUrl (bool): Whether to overwrite the whole url or not.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        return self._action(
            method=post,
            url=url,
            overwriteUrl=overwriteUrl,
            headers=headers,
            data=data,
            **kwargs
        )

    def put(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            overwriteUrl: bool = False,
            **kwargs
    ) -> Any:
        """
        Makes a PUT request to the RAWG API.

        Args:
            url (str): The URL to make the request to.
            data (Optional[Dict[str, Any]]): The data to pass to the request.
            headers (Optional[Dict[str, str]]): The headers to pass to the request.
            overwriteUrl (bool): Whether to overwrite the whole url or not.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        return self._action(
            method=put,
            url=url,
            overwriteUrl=overwriteUrl,
            headers=headers,
            data=data,
            **kwargs
        )

    def delete(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            overwriteUrl: bool = False,
            **kwargs
    ) -> Any:
        """
        Makes a DELETE request to the RAWG API.

        Args:
            url (str): The URL to make the request to.
            data (Optional[Dict[str, Any]]): The data to pass to the request.
            headers (Optional[Dict[str, str]]): The headers to pass to the request.
            overwriteUrl (bool): Whether to overwrite the whole url or not.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        return self._action(
            method=delete,
            url=url,
            params=data,
            overwriteUrl=overwriteUrl,
            headers=headers,
            **kwargs
        )

    def _action(
            self,
            method: Callable,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            overwriteUrl: bool = False,
            headers: Dict[str, Any] = None,
            **kwargs
    ) -> Any:
        """
        Makes a request to the RAWG API. This is a template method.

        Args:
            method (Callable): The requests function to use.
            url (str): The URL to make the request to.
            params (Optional[Dict[str, Any]]): The parameters to pass to the request.
            overwriteUrl (bool): Whether to use only use the URL or include the base URL.
            headers (Dict[str, Any]): Headers to pass to the request.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        # Create a unique ID for the request
        requestId: str = str(uuid4())

        # Set the URL
        url: str = f"{self.config.api.base}{"/" if not url.startswith("/") and not self.config.api.base.endswith("/") else ""}{url}" if not overwriteUrl else url

        # Yes this does have request context
        self.logger.info(
            f"{requestId} - {method.__name__.upper()} request to {url} with params {params} and kwargs {kwargs}"
        )

        # if url == "https://api.rawg.io/api/creators":
        #     return loads(
        #         "{\"count\": 27731, \"next\": \"https://api.rawg.io/api/creators?key=40b21226ee6c424dbb3b8aab167a1413&page=2&page_size=5\", \"previous\": \"None\", \"results\": [{\"id\": 31, \"name\": \"Gabe Newell\", \"slug\": \"gabe-newell\", \"image\": \"https://media.rawg.io/media/persons/5e5/5e5e064d3475fc3fe49d1d2debb4e36c.jpg\", \"image_background\": \"https://media.rawg.io/media/games/2ba/2bac0e87cf45e5b508f227d281c9252a.jpg\", \"games_count\": 24, \"positions\": [{\"id\": 2, \"name\": \"director\", \"slug\": \"director\"}, {\"id\": 5, \"name\": \"producer\", \"slug\": \"producer\"}, {\"id\": 7, \"name\": \"programmer\", \"slug\": \"programmer\"}], \"games\": [{\"id\": 4200, \"slug\": \"portal-2\", \"name\": \"Portal 2\", \"added\": 19217}, {\"id\": 4291, \"slug\": \"counter-strike-global-offensive\", \"name\": \"Counter-Strike: Global Offensive\", \"added\": 16891}, {\"id\": 13536, \"slug\": \"portal\", \"name\": \"Portal\", \"added\": 16366}, {\"id\": 12020, \"slug\": \"left-4-dead-2\", \"name\": \"Left 4 Dead 2\", \"added\": 16251}, {\"id\": 13537, \"slug\": \"half-life-2\", \"name\": \"Half-Life 2\", \"added\": 14544}, {\"id\": 19710, \"slug\": \"half-life-2-episode-one\", \"name\": \"Half-Life 2: Episode One\", \"added\": 10982}]}, {\"id\": 37, \"name\": \"Marc Laidlaw\", \"slug\": \"marc-laidlaw\", \"image\": \"https://media.rawg.io/media/persons/da3/da3fc907a3af9e494dc671b0c6348f5c.jpg\", \"image_background\": \"https://media.rawg.io/media/games/2ba/2bac0e87cf45e5b508f227d281c9252a.jpg\", \"games_count\": 15, \"positions\": [{\"id\": 1, \"name\": \"writer\", \"slug\": \"writer\"}], \"games\": [{\"id\": 4200, \"slug\": \"portal-2\", \"name\": \"Portal 2\", \"added\": 19217}, {\"id\": 4291, \"slug\": \"counter-strike-global-offensive\", \"name\": \"Counter-Strike: Global Offensive\", \"added\": 16891}, {\"id\": 13536, \"slug\": \"portal\", \"name\": \"Portal\", \"added\": 16366}, {\"id\": 12020, \"slug\": \"left-4-dead-2\", \"name\": \"Left 4 Dead 2\", \"added\": 16251}, {\"id\": 13537, \"slug\": \"half-life-2\", \"name\": \"Half-Life 2\", \"added\": 14544}, {\"id\": 10213, \"slug\": \"dota-2\", \"name\": \"Dota 2\", \"added\": 12323}]}, {\"id\": 63, \"name\": \"Robin Walker\", \"slug\": \"robin-walker\", \"image\": \"https://media.rawg.io/media/persons/b76/b76df211424e553218ce800f9b1d38f0.png\", \"image_background\": \"https://media.rawg.io/media/games/2ba/2bac0e87cf45e5b508f227d281c9252a.jpg\", \"games_count\": 14, \"positions\": [{\"id\": 6, \"name\": \"designer\", \"slug\": \"designer\"}], \"games\": [{\"id\": 4200, \"slug\": \"portal-2\", \"name\": \"Portal 2\", \"added\": 19217}, {\"id\": 4291, \"slug\": \"counter-strike-global-offensive\", \"name\": \"Counter-Strike: Global Offensive\", \"added\": 16891}, {\"id\": 13536, \"slug\": \"portal\", \"name\": \"Portal\", \"added\": 16366}, {\"id\": 12020, \"slug\": \"left-4-dead-2\", \"name\": \"Left 4 Dead 2\", \"added\": 16251}, {\"id\": 11859, \"slug\": \"team-fortress-2\", \"name\": \"Team Fortress 2\", \"added\": 13130}, {\"id\": 19710, \"slug\": \"half-life-2-episode-one\", \"name\": \"Half-Life 2: Episode One\", \"added\": 10982}]}, {\"id\": 27630, \"name\": \"David Speyrer\", \"slug\": \"david-speyrer\", \"image\": \"https://media.rawg.io/media/persons/513/51388ad8c1db829a2fcb0353560f0f2a.png\", \"image_background\": \"https://media.rawg.io/media/games/2ba/2bac0e87cf45e5b508f227d281c9252a.jpg\", \"games_count\": 12, \"positions\": [{\"id\": 7, \"name\": \"programmer\", \"slug\": \"programmer\"}], \"games\": [{\"id\": 4200, \"slug\": \"portal-2\", \"name\": \"Portal 2\", \"added\": 19217}, {\"id\": 13536, \"slug\": \"portal\", \"name\": \"Portal\", \"added\": 16366}, {\"id\": 12020, \"slug\": \"left-4-dead-2\", \"name\": \"Left 4 Dead 2\", \"added\": 16251}, {\"id\": 13537, \"slug\": \"half-life-2\", \"name\": \"Half-Life 2\", \"added\": 14544}, {\"id\": 19710, \"slug\": \"half-life-2-episode-one\", \"name\": \"Half-Life 2: Episode One\", \"added\": 10982}, {\"id\": 19709, \"slug\": \"half-life-2-episode-two\", \"name\": \"Half-Life 2: Episode Two\", \"added\": 10886}]}, {\"id\": 70, \"name\": \"Cris Velasco\", \"slug\": \"cris-velasco\", \"image\": \"https://media.rawg.io/media/persons/6ea/6ea06e2ddd6c0190e5134f61d826f30f.jpg\", \"image_background\": \"https://media.rawg.io/media/games/49c/49c3dfa4ce2f6f140cc4825868e858cb.jpg\", \"games_count\": 57, \"positions\": [{\"id\": 3, \"name\": \"composer\", \"slug\": \"composer\"}], \"games\": [{\"id\": 802, \"slug\": \"borderlands-2\", \"name\": \"Borderlands 2\", \"added\": 15004}, {\"id\": 4828, \"slug\": \"borderlands\", \"name\": \"Borderlands\", \"added\": 9603}, {\"id\": 17540, \"slug\": \"injustice-gods-among-us-ultimate-edition\", \"name\": \"Injustice: Gods Among Us Ultimate Edition\", \"added\": 9405}, {\"id\": 10243, \"slug\": \"company-of-heroes-2\", \"name\": \"Company of Heroes 2\", \"added\": 9321}, {\"id\": 3387, \"slug\": \"bloodborne\", \"name\": \"Bloodborne\", \"added\": 8469}, {\"id\": 480, \"slug\": \"resident-evil-7-biohazard\", \"name\": \"Resident Evil 7: Biohazard\", \"added\": 8196}]}]}",
        #         strict=False
        #     )

        # Add the API key to the data
        if params is None:
            params = {}

        params["key"] = self.config.api.key

        # Set the user agent
        if headers is None:
            headers = {}

        # Add the user agent header
        headers["User-Agent"] = f"AHSHS IA3 {self.config.server.owner.name}"
        headers["From"] = self.config.server.owner.email

        response: Response = method(
            url,
            params=params,
            **kwargs
        )

        response.raise_for_status()

        self.logger.debug(f"{requestId} - Response: {response.json()}")

        # Get the response data
        data: dict = response.json()

        # Edit the data to remove the API key from the next and previous URLs
        if "next" in data and data["next"] is not None:
            data["next"] = data["next"].replace(self.config.api.key, "KEY")

        if "previous" in data and data["previous"] is not None:
            data["previous"] = data["previous"].replace(self.config.api.key, "KEY")

        return data
