"""
Contains the Requester class.
"""

# Standard Library Imports
from typing import Any, Dict, Optional

# Third Party Imports
from requests import get, post, put, delete, Response

# Internal Imports
from .config import Config
from .logging import createLogger


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
        self.logger = createLogger("Requester", level=config.logging.level)

    def get(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs
    ) -> Any:
        """
        Makes a GET request to the RAWG API.

        Args:
            url (str): The URL to make the request to.
            params (Optional[Dict[str, Any]]): The parameters to pass to the request.
            headers (Optional[Dict[str, str]]): The headers to pass to the request.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        # Add the API key to the parameters
        if params is None:
            params = {}

        params["key"] = self.config.api.key

        result: Response = get(
            f"{self.config.api.base}/{url}",
            headers=headers,
            params=params,
            **kwargs
        )

        result.raise_for_status()
        return result.json()

    def post(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs
    ) -> Any:
        """
        Makes a POST request to the RAWG API.

        Args:
            url (str): The URL to make the request to.
            data (Optional[Dict[str, Any]]): The data to pass to the request.
            headers (Optional[Dict[str, str]]): The headers to pass to the request.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        # Add the API key to the data
        if data is None:
            data = {}

        data["key"] = self.config.api.key

        response: Response = post(
            f"{self.config.api.base}/{url}",
            headers=headers,
            data=data,
            **kwargs
        )

        response.raise_for_status()

        return response.json()

    def put(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs
    ) -> Any:
        """
        Makes a PUT request to the RAWG API.

        Args:
            url (str): The URL to make the request to.
            data (Optional[Dict[str, Any]]): The data to pass to the request.
            headers (Optional[Dict[str, str]]): The headers to pass to the request.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        # Add the API key to the data
        if data is None:
            data = {}

        data["key"] = self.config.api.key

        response: Response = put(
            f"{self.config.api.base}/{url}",
            headers=headers,
            data=data,
            **kwargs
        )

        response.raise_for_status()

        return response.json()

    def delete(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs
    ) -> Any:
        """
        Makes a DELETE request to the RAWG API.

        Args:
            url (str): The URL to make the request to.
            data (Optional[Dict[str, Any]]): The data to pass to the request.
            headers (Optional[Dict[str, str]]): The headers to pass to the request.
            **kwargs: Any additional keyword arguments to pass to the request.

        Returns:
            Any: The response from the RAWG API.
        """
        # Add the API key to the data
        if data is None:
            data = {}

        data["key"] = self.config.api.key

        response: Response = delete(
            f"{self.config.api.base}/{url}",
            headers=headers,
            data=data,
            **kwargs
        )

        response.raise_for_status()

        return response.json()
