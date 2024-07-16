"""
Contains infoBlueprint routes. Has urlPrefix of /.
"""
from datetime import date, timedelta

# Standard Library Imports

# Third Party Imports
from flask import render_template as renderTemplate
from flask.blueprints import Blueprint
from injector import inject

from server.internals.wrapper import API, Response

# Internal Imports

# Constants
infoBlueprint: Blueprint = Blueprint("info", __name__, url_prefix="/")


@infoBlueprint.get("/")
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
    trendingDates: list[date] = [
        date.today() - timedelta(days=30*12),
        date.today()
    ]

    trendingData: Response = api.game.list(dates=trendingDates, ordering="-metacritic", pageSize=6)  # Games between the start of the year and the end of the year ordering -added
    mostPopularTimespan: Response = api.game.list(dates=[date.fromisocalendar(day=7, week=51, year=2006), date.fromisocalendar(day=7, week=51, year=2008)], ordering="-metacritic", pageSize=6)  # Games between 1st jan 2007 and 31st dec 2007 ordering -added
    mostPopularAlltime: Response = api.game.list(ordering="-metacritic", pageSize=6)  # Most popular games all time

    return renderTemplate(
        "index.html",
        trending=trendingData.results,
        bestYear=mostPopularTimespan.results,
        popular=mostPopularAlltime.results,
    )


@infoBlueprint.get("/about")
def about() -> str:
    """
    The about page.

    Returns:
        str: The rendered about page.
    """
    return renderTemplate("info/about.html")
