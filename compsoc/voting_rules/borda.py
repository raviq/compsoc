"""
Computes the Borda score for a candidate.
"""


def borda_rule(profile, candidate: int) -> int:
    """
    Parameters: candidate (base candidate for scoring)
    """
    # Max score to be applied with borda count
    top_score = len(profile.candidates) - 1

    # Get pairwise scores
    scores = [pair[0] * (top_score - pair[1].index(candidate)) for
              pair in profile.pairs]

    # Return the total score
    return sum(scores)
