"""
Variation on Borda, with a decay (gamma).
Author: Shunsuke O.
"""
from typing import Callable
from compsoc.profile import Profile


def get_borda_gamma(gamma: float = 0.5) -> Callable[[int], float]:
    """
    Returns a callable function for the Borda gamma method with the specified gamma.

    :param gamma: The decay factor for Borda gamma, defaults to 0.5.
    :type gamma: float, optional
    :return: A callable function for the Borda gamma method.
    :rtype: Callable[[int], float]
    """

    def borda_gamma(profile: Profile, candidate: int) -> float:
        """
        Calculates the Borda gamma (decay) score for a candidate
        based on a profile. Author: Shunsuke O.

        :param profile: The voting profile.
        :type profile: VotingProfile
        :param candidate: The base candidate for scoring.
        :type candidate: int
        :return: The Borda gamma score for the candidate.
        :rtype: float
        """
        scores = [pair[0] * (gamma ** pair[1].index(candidate))
                  for pair in profile.pairs]
        return sum(scores)

    return borda_gamma
