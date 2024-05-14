"""
Contains infoBlueprint routes. Has urlPrefix of /games.
"""

# Standard Library Imports

# Third Party Imports
from flask.blueprints import Blueprint
from flask_injector import inject

# Internal Imports
from ..helpers import renderTemplate

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


@gamesBlueprint.get("/<string:gameId>")
@inject
def game(
        gameId: str
) -> str:
    """
    The game page.

    Args:
        gameId (str): The ID of the game to render.

    Returns:
        str: The rendered game page.
    """
    return renderTemplate(
        "games/game.html",
        gameId=gameId
    )
