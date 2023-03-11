"""
Useful schemas for classes used in the project
"""
from pydantic import BaseModel
from typing import Tuple


class Pair(BaseModel):
    """
    Defines a frequnecy, which is the number of times a ballot appears
    and the ballot in question, which ranks the candidates
    """
    frequency: int
    ballot: Tuple[int, ...]

    def __repr__(self):
        return f"(freq: {self.frequency}, {self.ballot})"
