"""
Computes the Dowdall score for a candidate.
"""
from compsoc.profile import Profile


def dowdall_rule(profile: Profile, candidate: int) -> int:
    """
    Calculates the Dowdall score for a candidate based on a profile.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The Dowdall score for the candidate.
    :rtype: int
    """
    top_score = len(profile.candidates) - 1
    # Get pairwise scores
    scores = [pair[0] * ((top_score - pair[1].index(candidate)) / (
            pair[1].index(candidate) + 1))
              for pair in profile.pairs]
    # Return the total score
    return sum(scores)
