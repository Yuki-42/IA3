"""
Initializes the routes for the server.
"""

from .info import infoBlueprint
from .games import gamesBlueprint
from .tests import testsBlueprint

__all__ = [
    "infoBlueprint",
    "gamesBlueprint",
    "testsBlueprint"
]
