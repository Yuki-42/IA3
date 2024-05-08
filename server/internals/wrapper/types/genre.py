"""
Contains the Genre class.
"""

# Standard Library Imports
from typing import Optional

# Third Party Imports
from pydantic import BaseModel


class Genre(BaseModel):
    """
    Represents a genre.
    """
    id: int
    name: str
    slug: str
    games_count: int
    image_background: str
    description: Optional[str] = None
