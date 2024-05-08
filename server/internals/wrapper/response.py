"""
Contains the Response class.
"""

# Standard Library Imports
from typing import List, Optional, Dict

# Third Party Imports
from pydantic import BaseModel

# Internal Imports
from .types import *


class Response:
    """
    Represents a response.
    """
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[Creator | Developer | Game | Genre | Platform | Publisher | Store | Tag]

    def __iter__(self) -> iter:
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __init__(
            self,
            data: Dict,
            results: List[Creator | Developer | Game | Genre | Platform | Publisher | Store | Tag]
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
