"""
Contains infoBlueprint routes. Has urlPrefix of /games.
"""

# Standard Library Imports
from datetime import datetime

# Third Party Imports
from flask import request, jsonify
from flask.blueprints import Blueprint

# Internal Imports
from ..helpers import renderTemplate

# Constants
gamesBlueprint: Blueprint = Blueprint("games", __name__, url_prefix="/games")


# Routes
@gamesBlueprint.route("/")
def games() -> str:
    """
    The games page.

    Returns:
        str: The rendered games page.
    """
    return renderTemplate("games/index.html")


@gamesBlueprint.route("/<string:gameId>")
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
