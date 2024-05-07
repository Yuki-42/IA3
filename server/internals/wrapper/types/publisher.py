"""
Contains the Publisher class.
"""

# Standard Library Imports
from typing import List, Dict, Optional
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel


class Publisher(BaseModel):
    """
    Represents a publisher.
    """
    id: Optional[int] = None
    name: str
    slug: str
    games_count: Optional[int] = None
    image_background: str
    