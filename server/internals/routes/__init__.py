"""
Initializes the routes for the server.
"""

from .api import apiBlueprint
from .errors import errorsBlueprint
from .games import gamesBlueprint
from .info import infoBlueprint
from .tests import testsBlueprint

__all__ = [
    "infoBlueprint",
    "gamesBlueprint",
    "testsBlueprint",
    "apiBlueprint",
    "errorsBlueprint"
]
