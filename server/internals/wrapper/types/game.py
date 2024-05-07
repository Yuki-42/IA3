"""
Contains the Game class.
"""

# Standard Library Imports
from typing import List, Dict, Optional
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel


class MetacriticPlatform(BaseModel):
    """
    Represents a metacritic platform.
    """
    metascore: Optional[int] = None
    url: str


class Game(BaseModel):
    """
    Represents a game.
    """
    slug: str
    name: str
    name_original: Optional[str] = None
    description: str
    metacritic: Optional[int] = None
    metacritic_platforms: Optional[List[MetacriticPlatform]] = None
    released: Optional[datetime] = None
    tba: Optional[bool] = None
    updated: Optional[datetime] = None
    background_image: Optional[str] = None
    background_image_additional: Optional[str] = None
    website: str
    rating: float
    rating_top: int
    ratings: Optional[List]  # TODO: Get the details of this
    reactions: Optional[List]  # TODO: Get the details of this
    added: Optional[int] = None
