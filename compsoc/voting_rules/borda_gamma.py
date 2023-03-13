"""
Variation on Borda, with a decay (gamma).
Author: Shunsuke O.
"""
from compsoc.decorators import rename
from typing import Callable


def get_borda_gamma(gamma: float = 0.5) -> Callable[[int], float]:
    @rename(f"Borda Gamma ({gamma})")
    def borda_gamma(profile, candidate: int) -> float:
        """
        Variation on Borda, with a decay (gamma).
        Author: Shunsuke O.
        Parameters: candidate (base candidate for scoring)
        """
        scores = [pair[0] * (gamma ** pair[1].index(candidate))
                  for pair in profile.pairs]
        return sum(scores)

    return borda_gamma
