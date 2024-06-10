"""
Contains the Store class.
"""

# Standard Library Imports
from typing import Optional

# Third Party Imports
from pydantic import BaseModel


class Store(BaseModel):
    """
    Represents a store.
    """
    id: int
    name: str
    slug: str
    domain: Optional[str] = None
    games_count: Optional[int] = None
    image_background: Optional[str] = None
    description: Optional[str] = None
