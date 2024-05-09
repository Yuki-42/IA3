"""
Initializes the routes for the server.
"""

from .info import infoBlueprint
from .games import gamesBlueprint
from .tests import testsBlueprint
from .api import apiBlueprint
from .errors import errorsBlueprint

__all__ = [
    "infoBlueprint",
    "gamesBlueprint",
    "testsBlueprint",
    "apiBlueprint",
    "errorsBlueprint"
]
