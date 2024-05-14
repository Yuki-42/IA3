"""
Contains the Developer class.
"""

# Standard Library Imports
from typing import Optional

# Third Party Imports
from pydantic import BaseModel


# Local Imports


class Developer(BaseModel):
    """
    Represents a developer.
    """
    id: Optional[int] = None
    name: str
    slug: str
    games_count: Optional[int] = None
    image_background: str
    description: str
