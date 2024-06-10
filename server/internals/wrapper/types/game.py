"""
Contains the Game class.
"""
# Standard Library Imports
from datetime import date, datetime
from json import dumps
from typing import Any, Dict, List, Literal, Optional
from re import compile

# Third Party Imports
from pydantic import BaseModel

# Internal Imports
from .store import Store
from .tag import Tag
from .developer import Developer
from .genre import Genre
from .publisher import Publisher


# CONSTANTS
breakTag = compile(r"<\s*br\s*(/)?>")  # Pre-compile the regex for br tags at application startup to save time


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

    class PlatformType(BaseModel):
        id: int
        name: str
        slug: str
        image: Optional[str | None] = None
        year_end: Optional[int | None] = None
        year_start: Optional[int | None] = None
        games_count: Optional[int | None] = None
        image_background: Optional[str | None] = None

    platform: PlatformType
    released_at: Optional[date | None] = None
    requirements_en: Optional[Requirement | None] = None
    requirements_ru: Optional[Requirement | None] = None


class GStore(BaseModel):
    """
    Represents a store as returned from a game.
    """
    id: Optional[int] = None
    store: Store


class GShortScreenshot(BaseModel):
    """
    Represents a short screenshot.
    """
    id: int
    image: str


class Game(BaseModel):
    """
    Represents a game returned from a search.
    """
    id: int
    slug: str
    name: str
    description: Optional[str] = None
    released: datetime | None
    tba: bool
    background_image: Optional[str] = None
    rating: float
    rating_top: int
    ratings: List
    ratings_count: int
    reviews_text_count: int
    added: int
    added_by_status: Any
    metacritic: Optional[int] = None
    playtime: int
    suggestions_count: int
    updated: datetime
    esrb_rating: EsrbRating | None
    user_game: Any
    reviews_count: int
    community_rating: Optional[int] = None
    saturated_color: str
    dominant_color: str
    platforms: List[Platform]
    parent_platforms: Optional[List[Platform]] = None
    genres: Optional[List[Genre]] = None
    stores: Optional[List[GStore]] = None
    clip: Any
    tags: List[Tag]
    developers: Optional[List[Developer]] = None
    publishers: Optional[List[Publisher]] = None
    short_screenshots: Optional[List[GShortScreenshot]] = None

    def __init__(self, **data):
        print(dumps(data, indent=4))

        # Remove any newlines from the description
        if "description" in data:
            data["description"] = data["description"].replace("\n", " ")
            data["description"] = breakTag.subn("", data["description"])

        super().__init__(**data)


class DetailedGame(BaseModel):
    """
    Represents a game returned from a details query.
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
    developers: Optional[List] = None  # TODO: Get the details of this
    genres: Optional[List[Genre]] = None  # TODO: Get the details of this
    tags: Optional[List[Tag]] = None
    publishers: Optional[List[Publisher]] = None  # TODO: Get the details of this
