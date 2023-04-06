"""
Computes the Copeland score for a candidate.
"""
import numpy as np


def copeland_rule(profile, candidate: int) -> int:
    """
    Calculates the Copeland score for a candidate based on a profile.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The Copeland score for the candidate.
    :rtype: int
    """
    scores = []
    for m in profile.candidates:
        preference = profile.get_net_preference(candidate,
                                                m)  # preference over m
        scores.append(np.sign(preference))  # win or not
    # Return the total score
    return sum(scores)
