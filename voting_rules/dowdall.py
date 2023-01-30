"""
Computes the Dowdall score for a candidate.
"""
from typing import Callable, Set

def create_rule(profile: Set[int]) -> Callable[[int], int]:
    def dowdall_rule(candidate: int) -> int:
        """
        Parameters: candidate (base candidate for scoring)
        """
        top_score = len(profile.candidates) - 1
        # Get pairwise scores
        scores = [n_votes * ((top_score - ballot.index(candidate)) / (ballot.index(candidate) + 1))
                    for n_votes, ballot in profile.pairs]
        # Return the total score
        return sum(scores)
    dowdall_rule.__name__ = 'dowdall'
    return dowdall_rule
