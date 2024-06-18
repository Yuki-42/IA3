"""
Contains infoBlueprint routes. Has urlPrefix of /games.
"""

# Standard Library Imports

# Third Party Imports
from flask import request, render_template as renderTemplate
from flask.blueprints import Blueprint
from flask_injector import inject

# Internal Imports
from .api import API
from ..wrapper import Game
from ..wrapper.response import Response

# Constants
gamesBlueprint: Blueprint = Blueprint("games", __name__, url_prefix="/games")


# Routes
@gamesBlueprint.get("/")
@inject
def index(
        api: API,
) -> str:
    """
    The games page.

    Returns:
        str: The rendered games page.
    """
    # Need trending, most popular (2007), Most popular of all time
    trendingData: Response = api.game.list(dates=[], ordering="-rating")  # Games between the start of the year and the end of the year ordering -added
    mostPopularTimespan: Response = api.game.list(ordering="-rating")  # Games between 1st jan 2007 and 31st dec 2007 ordering -added
    mostPopularAlltime: Response = api.game.list(ordering="-rating")  # Most popular games all time

    return renderTemplate(
        "games/index.html",
        trending=trendingData,
        dateRange=mostPopularTimespan,
        mostPopular=mostPopularAlltime,
    )


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
    gameData: Game = api.game.details(gameId)

    try:
        # Check request cookies for age
        age: int = request.cookies.get("age", 0, int)
    except TypeError:
        age: int = 0

    if gameData.esrb_rating is None:
        return renderTemplate(
            "games/game.html",
            game=api.game.details(gameId)
        )

    if gameData.esrb_rating.slug == "adults-only" and age < 18:
        return renderTemplate("games/age.html", requiredAge=18)

    if gameData.esrb_rating.slug == "mature" and age < 17:
        return renderTemplate("games/age.html", requiredAge=17)

    return renderTemplate(
        "games/game.html",
        game=api.game.details(gameId)
    )
