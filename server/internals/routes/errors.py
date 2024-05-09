"""
Contains errors routes.
"""

# Standard Library Imports
from datetime import datetime

# Third Party Imports
from flask import request, jsonify
from flask.blueprints import Blueprint
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound

# Internal Imports
from ..helpers import renderTemplate

# Create error blueprint
errorsBlueprint: Blueprint = Blueprint("errors", __name__, url_prefix="/errors")


# Routes
@errorsBlueprint.app_errorhandler(400)
def badRequest(
        error: BadRequest
) -> str:
    """
    The bad request page.

    Args:
        error (BadRequest): The error to render.

    Returns:
        str: The rendered bad request page.
    """
    return renderTemplate(
        "error.html",
        error=error
    )


@errorsBlueprint.app_errorhandler(401)
def unauthorized(
        error: Unauthorized
) -> str:
    """
    The unauthorized page.

    Args:
        error (Unauthorized): The error to render.

    Returns:
        str: The rendered unauthorized page.
    """
    return renderTemplate(
        "error.html",
        error=error
    )


@errorsBlueprint.app_errorhandler(403)
def forbidden(
        error: Forbidden
) -> str:
    """
    The forbidden page.

    Args:
        error (Unauthorized): The error to render.

    Returns:
        str: The rendered forbidden page.
    """
    return renderTemplate(
        "error.html",
        error=error
    )


@errorsBlueprint.app_errorhandler(404)
def notFound(
        error: NotFound
) -> str:
    """
    The not found page.

    Args:
        error (NotFound): The error to render.

    Returns:
        str: The rendered not found page.
    """
    return renderTemplate(
        "error.html",
        error=error
    )
