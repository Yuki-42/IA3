"""
Contains infoBlueprint routes. Has urlPrefix of /.
"""

# Standard Library Imports

# Third Party Imports
from flask.blueprints import Blueprint

# Internal Imports
from ..helpers import renderTemplate

# Constants
infoBlueprint: Blueprint = Blueprint("info", __name__, url_prefix="/")


@infoBlueprint.get("/")
def index() -> str:
    """
    The index page.

    Returns:
        str: The rendered index page.
    """
    return renderTemplate("info/index.html")


@infoBlueprint.get("/about")
def about() -> str:
    """
    The about page.

    Returns:
        str: The rendered about page.
    """
    return renderTemplate("info/about.html")
