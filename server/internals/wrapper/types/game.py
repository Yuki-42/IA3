"""
Contains the Game class.
"""

# Standard Library Imports
from typing import List, Dict, Optional, Literal
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel


# Internal Imports


class MetacriticPlatform(BaseModel):
    """
    Represents a metacritic platform.
    """
    metascore: Optional[int] = None
    url: str


class EsrbRating(BaseModel):
    """
    Represents an ESRB rating.
    """
    id: int
    slug: Literal["everyone", "everyone-10-plus", "teen", "mature", "adults-only", "rating-pending"]
    name: Literal["Everyone", "Everyone 10+", "Teen", "Mature", "Adults Only", "Rating Pending"]


class Requirement(BaseModel):
    """
    Represents a requirement.
    """
    minimum: Optional[str] = None
    recommended: Optional[str] = None


class Platform(BaseModel):
    """
    Represents a platform.
    """
    platform: Dict
    released_at: Optional[datetime] = None
    requirements: Optional[Requirement]  # TODO: Get the details of this


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
    added_by_status: Optional[Dict]  # TODO: Get the details of this
    playtime: Optional[int] = None
    screenshots_count: Optional[int] = None
    movies_count: Optional[int] = None
    creators_count: Optional[int] = None
    achievements_count: Optional[int] = None
    parent_achievements_count: Optional[int] = None
    reddit_url: Optional[str] = None
    reddit_name: Optional[str] = None
    reddit_description: Optional[str] = None
    reddit_logo: Optional[str] = None
    reddit_count: Optional[int] = None
    twitch_count: Optional[int] = None
    youtube_count: Optional[int] = None
    reviews_text_count: Optional[int] = None
    ratings_count: Optional[int] = None
    suggestions_count: Optional[int] = None
    alternative_names: Optional[List[str]] = None
    metacritic_url: Optional[str] = None
    parents_count: Optional[int] = None
    additions_count: Optional[int] = None
    game_series_count: Optional[int] = None
    esrb_rating: Optional[EsrbRating] = None
    platforms: Optional[List[Platform]] = None  # This platform is a different platform to ./platform.py
