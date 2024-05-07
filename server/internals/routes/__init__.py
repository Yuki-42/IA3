"""
Initializes the routes for the server.
"""

from .info import infoBlueprint
from .games import gamesBlueprint

__all__ = [
    "infoBlueprint",
    "gamesBlueprint"
]
