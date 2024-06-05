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
