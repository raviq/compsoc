"""
Computes the Simpson score for a candidate.
"""
from compsoc.decorators import rename


@rename("Simpson")
def simpson_rule(profile, candidate: int) -> int:
    """
    Calculates the minimum pairwise score of a candidate using the Simpson rule.
    Parameters: candidate (base candidate for scoring)
    Returns: The minimum pairwise score of the candidate among all other
    candidates.
    """
    # Get pairwise scores
    scores = [profile.get_net_preference(candidate, m) for m in
              profile.candidates - {candidate}]
    # Return the minimum score in scores
    return min(scores)
