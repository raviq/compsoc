"""
Borda random
"""
import random


def borda_random_gamma(profile, candidate: int) -> float:
    """
    Calculates the Borda random decay (gamma) score for a
    candidate based on a profile.
    Author: Shunsuke O.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The Borda random gamma score for the candidate.
    :rtype: float
    """
    gamma = random.random()
    scores = [pair[0] * (gamma ** pair[1].index(candidate))
              for pair in profile.pairs]
    return sum(scores)
