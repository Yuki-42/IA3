"""
Contains apiBlueprint routes. Has urlPrefix of /api. Soley for forwarding requests to RAWG without exposing the API key.
"""

# Standard Library Imports

# Third Party Imports
from flask import request
from flask.blueprints import Blueprint
from flask_injector import inject
from werkzeug.exceptions import Unauthorized

# Internal Imports
from .. import Config
from ..wrapper import API

apiBlueprint: Blueprint = Blueprint("api", __name__, url_prefix="/api")


# Create one route that consumes the url and forwards it to the RAWG API
@apiBlueprint.get("/<path:url>", strict_slashes=False)
@inject
def index(
        url: str,
        api: API,
        config: Config
) -> str:
    """
    The API forwarding route. Requests have to come from the server itself.

    Args:
        url (str): The URL to forward to the RAWG API.
        api (API): The API wrapper to use (injected).
        config (Config): The configuration object (injected).

    Returns:
        str: The response from the RAWG API.
    """
    if request.remote_addr != config.server.host and config.server.debug is False:
        raise Unauthorized("Requests to the API must come from the server itself.")

    return api.requester.get(url)

