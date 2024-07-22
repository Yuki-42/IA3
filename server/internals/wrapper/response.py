"""
Contains the Response class.
"""

# Standard Library Imports
from typing import Dict, List, Optional

from pydantic import BaseModel

# Internal Imports
from .types import *


# Third Party Imports


class Response:
    """
    Represents a response.
    """
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[BaseModel]

    def __iter__(self) -> iter:
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __init__(
            self,
            data: Dict,
            results: List[BaseModel]
    ) -> None:
        """
        Initializes the Response class.

        Args:
            data (Dict): The data to use.
            results (List[Creator | Developer | Game | Genre | Platform | Publisher | Store | Tag]): The results to use.
        """
        self.count = data["count"]
        self.next = data["next"]
        self.previous = data["previous"]
        self.results = results
