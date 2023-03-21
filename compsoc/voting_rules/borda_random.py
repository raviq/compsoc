import random
from compsoc.decorators import rename


@rename("Borda Random Gamma")
def borda_random_gamma(profile, candidate: int) -> float:
    """
    Variation on Borda, with a decay (gamma).
    Author: Shunsuke O.
    Parameters: candidate (base candidate for scoring)
    """
    gamma = random.random()
    scores = [pair[0] * (gamma ** pair[1].index(candidate))
              for pair in profile.pairs]
    return sum(scores)
