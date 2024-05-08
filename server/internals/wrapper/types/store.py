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
    domain: str
    games_count: int
    image_background: str
    description: Optional[str] = None
