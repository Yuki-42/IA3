"""
Contains the Creator class.
"""

# Standard Library Imports
from typing import List, Dict, Optional
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel


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
