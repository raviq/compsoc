"""
Computes the Copeland score for a candidate.
"""
import numpy as np
from decorators import rename

@rename("Copeland")
def copeland_rule(profile, candidate: int) -> int:
    """
    Parameters: candidate (base candidate for scoring)
    """
    scores = []
    for m in profile.candidates:
        preference = profile.get_net_preference(candidate,
                                                m)  # preference over m
        scores.append(np.sign(preference))  # win or not
    # Return the total score
    return sum(scores)
