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
    url: Optional[str] = None
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
    ratings_count: int
    reactions: Optional[dict[str, int]] = None  # TODO: Get the details of this
    added: int
    added_by_status: Optional[dict[str, int]] = None  # TODO: Get the details of this
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


class User(BaseModel):
    """
    Represents a user.
    """
    id: int
    username: str
    slug: str
    full_name: str
    avatar: Optional[str] = None
    games_count: int
    collections_count: int


class Review(BaseModel):
    """
    Represents a review.
    """
    id: int
    user: User
    game: int
    text: str
    text_preview: str
    text_previews: List[str]
    text_attachments: int
    rating: int
    reactions: dict[str, int]
    created: datetime
    edited: datetime
    likes_count: int
    likes_positive: int
    likes_rating: int
    comments_count: int
    comments_parent_count: int
    posts_count: int
    share_image: str
    is_text: bool
    external_avatar: Optional[str] = None
    comments: dict[str, Any]
    can_delete: bool
