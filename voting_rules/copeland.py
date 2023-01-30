"""
Computes the Copeland score for a candidate.
"""
from typing import Callable, Set
import numpy as np

def create_rule(profile: Set[int]) -> Callable[[int], int]:
    def copeland_rule(candidate: int) -> int:
        """
        Parameters: candidate (base candidate for scoring)
        """
        scores = list()
        for m in profile.candidates:
            preference = profile.net_preference(candidate, m) # preference over m
            scores.append(np.sign(preference))                # win or not
        # Return the total score
        return sum(scores)
    copeland_rule.__name__ = 'copeland'
    return copeland_rule
