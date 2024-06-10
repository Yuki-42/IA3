"""
Contains the Platform class.
"""

# Standard Library Imports
from typing import Optional

# Third Party Imports
from pydantic import BaseModel


class Platform(BaseModel):
    """
    Represents a platform.
    """
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    games_count: Optional[int] = None
    image_background: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None
