"""
Contains the Response class.
"""

# Standard Library Imports
from typing import List, Optional

# Third Party Imports
from pydantic import BaseModel

# Internal Imports
from .developer import Developer
from .game import Game


class Response(BaseModel):
    """
    Represents a response.
    """
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[Game | Developer]