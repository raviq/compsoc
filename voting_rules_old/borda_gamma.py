"""
Variation on Borda, with a decay (gamma).
Author: Shunsuke O.
"""
from typing import Callable, Set

def create_rule(profile: tuple, gamma: float = 0.5) -> Callable[[int], float]:
    def borda_gamma(candidate: int) -> float:
        """
        Parameters: candidate (base candidate for scoring)
        """
        scores = [n_votes * (gamma ** ballot.index(candidate))
                    for n_votes, ballot in profile.pairs]
        return sum(scores)
    borda_gamma.__name__ = f'borda({gamma})'
    return borda_gamma
