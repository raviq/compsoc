"""
Computes the Simpson score for a candidate.
"""


def simpson_rule(profile, candidate: int) -> int:
    """
    Calculates the minimum pairwise score of a candidate using the Simpson rule.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The minimum pairwise score of the candidate among all other candidates.
    :rtype: int
    """
    # Get pairwise scores
    scores = [profile.get_net_preference(candidate, m) for m in
              profile.candidates - {candidate}]
    # Return the minimum score in scores
    return min(scores)
