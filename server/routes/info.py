"""
Contains info routes. Has urlPrefix of /.
"""

# Standard Library Imports
from datetime import datetime

# Third Party Imports
from flask import request, jsonify
from flask.blueprints import Blueprint

# Internal Imports
from ..internals.helpers import renderTemplate

# Constants
info = Blueprint("info", __name__, url_prefix="/")


@info.route("/")
def index() -> str:
    """
    The index page.

    Returns:
        str: The rendered index page.
    """
    return renderTemplate("info/index.html")


@info.route("/about")
def about() -> str:
    """
    The about page.

    Returns:
        str: The rendered about page.
    """
    return renderTemplate("info/about.html")

