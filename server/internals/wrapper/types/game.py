"""
Contains the Game class.
"""
# Standard Library Imports
from datetime import date, datetime
from re import compile
from typing import Any, List, Literal, Optional

# Third Party Imports
from pydantic import BaseModel

# Internal Imports
from .developer import Developer
from .genre import Genre
from .platform import Platform
from .publisher import Publisher
from .store import Store
from .tag import Tag

# CONSTANTS
breakTag = compile(r"<\s*br\s*(/)?>")  # Pre-compile the regex for br tags at application startup to save time


# Temporary helper function
# def getJsonDifference(
#         json1: Dict[str, Any],
#         json2: Dict[str, Any]
# ) -> None:
#     """
#     Prints any missing keys in json2 compared to json1. Also prints mismatched values. Works recursively on both lists and dictionaries.
#
#     Args:
#         json1 (Dict[str, Any]): The first JSON object. Considered the "correct" JSON object.
#         json2 (Dict[str, Any]): The second JSON object.
#     """
#     for key in json1:
#         if key not in json2:
#             print(f"Key {key} is missing from json2")
#         elif isinstance(json1[key], dict):
#             getJsonDifference(json1[key], json2[key])
#         elif json1[key] != json2[key]:
#             print(f"Key {key} has a mismatched value. Expected:\n {dumps(json1[key], indent=4)} \n Got:\n {json2[key]}")


class MetacriticPlatform(BaseModel):
    """
    Represents a metacritic platform.
    """

    class MPlatform(BaseModel):
        """
        Represents a metacritic platform.
        """
        platform: int
        name: str
        slug: str

    metascore: Optional[int] = None
    url: str
    platform: MPlatform


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


class GPlatform(BaseModel):
    """
    Represents a platform.
    """
    platform: Platform
    released_at: Optional[date | None] = None
    requirements: Optional[Requirement | None] = None
    requirements_en: Optional[Requirement | None] = None
    requirements_ru: Optional[Requirement | None] = None


class PPlatform(BaseModel):
    """
    Represents a parent platform.
    """

    class NPlatform(BaseModel):
        """
        Represents a nested platform.
        """
        id: int
        name: str
        slug: str

    platform: NPlatform


class GStore(BaseModel):
    """
    Represents a store as returned from a game.
    """
    id: Optional[int] = None
    url: Optional[str]
    store: Store


class GShortScreenshot(BaseModel):
    """
    Represents a short screenshot.
    """
    id: int
    image: str


class Rating(BaseModel):
    """
    Represents a rating.
    """
    id: int
    title: str
    count: int
    percent: float


class Game(BaseModel):
    """
    Represents a game returned from a search.
    """
    id: int
    slug: str
    name: str
    name_original: Optional[str] = None
    description: Optional[str] = None
    metacritic: Optional[int] = None
    metacritic_platforms: Optional[List[MetacriticPlatform]] = None
    released: Optional[date] = None
    tba: Optional[bool] = None
    updated: Optional[datetime] = None
    background_image: Optional[str] = None
    background_image_additional: Optional[str] = None
    website: Optional[str] = None
    rating: float
    rating_top: int
    ratings: List[Rating]

    # This probably goes here
    ratings_count: int

    reactions: Optional[dict[str, int]]  # TODO: Get the details of this
    added: int
    added_by_status: Optional[dict[str, int]]  # TODO: Get the details of this
    playtime: Optional[int] = None
    screenshots_count: int
    movies_count: int
    creators_count: int
    achievements_count: int
    parent_achievements_count: int
    reddit_url: Optional[str] = None
    reddit_name: Optional[str] = None
    reddit_description: Optional[str] = None
    reddit_logo: Optional[str] = None
    reddit_count: int
    twitch_count: int
    youtube_count: int
    reviews_text_count: int
    ratings_count: int
    suggestions_count: int
    alternative_names: List[str]
    metacritic_url: Optional[str] = None
    parents_count: int
    additions_count: int
    game_series_count: int
    user_game: Optional[Any] = None  # TODO: Get the details of this
    reviews_count: int
    saturated_color: str
    dominant_color: str

    parent_platforms: Optional[List[PPlatform]] = None
    platforms: List[GPlatform]
    released_at: Optional[date] = None
    requirements: Optional[Requirement] = None

    suggestions_count: int
    esrb_rating: Optional[EsrbRating] = None
    community_rating: Optional[int] = None

    genres: Optional[List[Genre]] = None
    stores: Optional[List[GStore]] = None
    clip: Any
    tags: List[Tag]
    developers: Optional[List[Developer]] = None
    publishers: Optional[List[Publisher]] = None
    short_screenshots: Optional[List[GShortScreenshot]] = None

    screenshots_count: Optional[int] = None
    movies_count: Optional[int] = None
    creators_count: Optional[int] = None
    achievements_count: Optional[int] = None
    parent_achievements_count: Optional[int] = None
    reddit_count: Optional[int] = None
    twitch_count: Optional[int] = None
    youtube_count: Optional[int] = None
    reviews_text_count: Optional[int] = None
    ratings_count: Optional[int] = None
    suggestions_count: Optional[int] = None
    alternative_names: Optional[List[str]] = None
    parents_count: Optional[int] = None
    additions_count: Optional[int] = None
    game_series_count: Optional[int] = None
    tags: Optional[List[Tag]] = None
    description_raw: Optional[str] = None

    def __init__(
            self,
            **data
    ) -> None:
        # Remove any newlines from the description
        if "description" in data:
            data["description"] = data["description"].replace("\n", " ")
            data["description"] = breakTag.subn("", data["description"])[0]

        super().__init__(**data)
        # getJsonDifference(data, self.dict())


class DetailedGame(BaseModel):
    """
    Represents a game returned from a details query.
    """
