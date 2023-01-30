"""
Computes the Simpson score for a candidate.
"""
from typing import Callable, Set

def create_rule(profile: Set[int]) -> Callable[[int], int]:
    def simpson_rule(candidate: int) -> int:
        """
        Calculates the minimum pairwise score of a candidate using the Simpson rule.
        Parameters: candidate (base candidate for scoring)
        Returns: The minimum pairwise score of the candidate among all other candidates.
        """
        # Get pairwise scores
        scores = [profile.net_preference(candidate, m) for m in profile.candidates - {candidate}]
        # Return the minimum score in scores
        return min(scores)
    simpson_rule.__name__ = 'simpson'
    return simpson_rule
