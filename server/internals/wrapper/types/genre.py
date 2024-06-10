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
    games_count: Optional[int] = None
    image_background: Optional[str] = None
    description: Optional[str] = None
