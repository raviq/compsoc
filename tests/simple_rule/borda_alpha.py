from compsoc.profile import Profile
from typing import Callable

# Sample rule

def get_borda_alpha(alpha: float = 0.5) -> Callable[[int], float]:
    """
    Returns a callable function for the Borda alpha method with the specified decay alpha.

    :param alpha: The decay factor for Borda alpha, defaults to 0.5.
    :type alpha: float, optional
    :return: A callable function for the Borda alpha method.
    :rtype: Callable[[int], float]
    """

    def borda_alpha(profile: Profile, candidate: int) -> float:
        """
        Calculates the Borda alpha (decay 2) score for a candidate
        :param profile: The voting profile.
        :type profile: VotingProfile
        :param candidate: The base candidate for scoring.
        :type candidate: int
        :return: The Borda alpha score for the candidate.
        :rtype: float
        """
        scores = [pair[0] * (alpha ** pair[1].index(candidate))
                  for pair in profile.pairs]
        return sum(scores)

    return borda_alpha
