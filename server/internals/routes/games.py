"""
Contains infoBlueprint routes. Has urlPrefix of /games.
"""

# Standard Library Imports

# Third Party Imports
from flask import request
from flask.blueprints import Blueprint
from flask_injector import inject

# Internal Imports
from ..helpers import renderTemplate
from .api import API
from ..wrapper.response import Response

# Constants
gamesBlueprint: Blueprint = Blueprint("games", __name__, url_prefix="/games")


# Routes
@gamesBlueprint.get("/")
@inject
def index() -> str:
    """
    The games page.

    Returns:
        str: The rendered games page.
    """
    return renderTemplate("games/index.html")


@gamesBlueprint.get("/search")
@inject
def search(
        api: API
) -> str:
    """
    Searches for games matching the query.

    Returns:
        str: The rendered search page.
    """
    args: dict = request.args.to_dict()

    match args.get("type", "list"):
        case "list":
            return renderTemplate(
                "games/index.html",
                response=api.game.list(**args)
            )


@gamesBlueprint.get("/<string:gameId>")
@inject
def game(
        gameId: str,
        api: API
) -> str:
    """
    The game page.

    Args:
        gameId (str): The ID of the game to render.
        api (API): The API object. (Injected)

    Returns:
        str: The rendered game page.
    """
    return renderTemplate(
        "games/game.html",
        game=api.game.details(gameId)
    )
