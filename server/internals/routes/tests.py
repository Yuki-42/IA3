"""
Contains testBlueprint routes. Has urlPrefix of /tests.
"""

# Standard Library Imports

# Third Party Imports
from flask.blueprints import Blueprint
from flask_injector import inject

# Internal Imports
from ..helpers import renderTemplate

# Constants
testsBlueprint: Blueprint = Blueprint("tests", __name__, url_prefix="/tests")


# Routes
@testsBlueprint.route("/", methods=["GET"])
def index() -> str:
    """
    The tests page. Displays all modules available for testing.

    Returns:
        str: The rendered tests page.
    """
    return renderTemplate("tests/index.html")


@testsBlueprint.route("/creator", methods=["GET"])
@inject
def creator() -> str:
    """
    The creator tests page.

    Returns:
        str: The rendered creator tests page.
    """
    return renderTemplate("tests/creator.html")
