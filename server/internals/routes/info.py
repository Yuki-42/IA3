"""
Contains infoBlueprint routes. Has urlPrefix of /.
"""

# Standard Library Imports

# Third Party Imports
from flask import render_template as renderTemplate
from flask.blueprints import Blueprint

# Internal Imports

# Constants
infoBlueprint: Blueprint = Blueprint("info", __name__, url_prefix="/")


@infoBlueprint.get("/")
def index() -> str:
    """
    The index page.

    Returns:
        str: The rendered index page.
    """
    return renderTemplate("index.html")


@infoBlueprint.get("/about")
def about() -> str:
    """
    The about page.

    Returns:
        str: The rendered about page.
    """
    return renderTemplate("info/about.html")
