"""
Computes the Borda score for a candidate.
"""
from typing import Callable, Set

def create_rule(profile: Set[int]) -> Callable[[int], int]:
    def borda_rule(candidate: int) -> int:
        # Max score to be applied with borda count
        top_score = len(profile.candidates) - 1
        # Get pairwise scores
        scores = [n_votes * (top_score - ballot.index(candidate)) for n_votes, ballot in profile.pairs]
        # Return the total score
        return sum(scores)
    borda_rule.__name__ = 'borda'
    return borda_rule
