"""
Computes the Dowdall score for a candidate.
"""
from compsoc.decorators import rename


@rename("Dowdall")
def dowdall_rule(profile, candidate: int) -> int:
    """
    Parameters: candidate (base candidate for scoring)
    """
    top_score = len(profile.candidates) - 1
    # Get pairwise scores
    scores = [pair[0] * ((top_score - pair[1].index(candidate)) / (
            pair[1].index(candidate) + 1))
              for pair in profile.pairs]
    # Return the total score
    return sum(scores)
