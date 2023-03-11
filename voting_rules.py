"""
Pre-defined voting rules
"""
import random
from decorators import rename
import numpy as np


@rename("Borda")
def borda_rule(profile, candidate: int) -> int:
    """
    Parameters: candidate (base candidate for scoring)
    """
    # Max score to be applied with borda count
    top_score = len(profile.candidates) - 1

    # Get pairwise scores
    scores = [pair.frequency * (top_score - pair.ballot.index(candidate)) for
              pair in profile.pairs]

    # Return the total score
    return sum(scores)


def get_borda_gamma(gamma: float):
    @rename(f"Borda Gamma ({gamma})")
    def borda_gamma(profile, candidate: int) -> float:
        """
        Variation on Borda, with a decay (gamma).
        Author: Shunsuke O.
        Parameters: candidate (base candidate for scoring)
        """
        scores = [pair.frequency * (gamma ** pair.ballot.index(candidate))
                  for pair in profile.pairs]
        return sum(scores)

    return borda_gamma


@rename("Borda Random Gamma")
def borda_random_gamma(profile, candidate: int) -> float:
    """
    Variation on Borda, with a decay (gamma).
    Author: Shunsuke O.
    Parameters: candidate (base candidate for scoring)
    """
    gamma = random.random()
    scores = [pair.frequency * (gamma ** pair.ballot.index(candidate))
              for pair in profile.pairs]
    return sum(scores)


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


@rename("Dowdall")
def dowdall_rule(profile, candidate: int) -> int:
    """
    Parameters: candidate (base candidate for scoring)
    """
    top_score = len(profile.candidates) - 1
    # Get pairwise scores
    scores = [pair.frequency * ((top_score - pair.ballot.index(candidate)) / (
            pair.ballot.index(candidate) + 1))
              for pair in profile.pairs]
    # Return the total score
    return sum(scores)


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


RULES = [borda_rule, copeland_rule, dowdall_rule, simpson_rule]
# Adding some extra Borda variants, with decay parameter
borda_variants = [get_borda_gamma(gamma) for gamma in
                  [1.0, 0.99, 0.75, 0.6, 0.25, 0.01]]
RULES.extend(borda_variants)
