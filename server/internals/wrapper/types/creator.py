"""
Contains the Creator class.
"""
# Standard Library Imports
from datetime import datetime
from typing import Optional

# Third Party Imports
from pydantic import BaseModel


# Local Imports


class Creator(BaseModel):
    """
    Represents a creator.
    """
    id: int
    name: str
    slug: str
    image_background: Optional[str] = None
    description: Optional[str] = None
    games_count: Optional[int] = None
    reviews_count: Optional[int] = None
    rating: Optional[float] = None
    rating_top: Optional[int] = None
    updated: Optional[datetime] = None
