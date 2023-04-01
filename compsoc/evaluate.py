"""
Evaluation functions
"""
from typing import List, Tuple, Callable

from compsoc.profile import Profile
from compsoc.voter_model import get_profile_from_model
from compsoc.voting_rules.borda import borda_rule
from compsoc.voting_rules.borda_gamma import get_borda_gamma
from compsoc.voting_rules.copeland import copeland_rule
from compsoc.voting_rules.dowdall import dowdall_rule
from compsoc.voting_rules.simpson import simpson_rule


def voter_subjective_utility_for_elected_candidate(elected: List[int], vote: Tuple[int],
                                                   topn: int) -> tuple:
    """
    Calculates the subjective utility of an individual voter for an elected candidate.

    :param elected: List of elected candidates.
    :type elected: List[int]
    :param vote: A tuple containing a voter's ranked candidates.
    :type vote: Tuple[int]
    :param topn: The number of top candidates to consider for utility calculation.
    :type topn: int
    :return: A tuple containing utility for the top candidate and total utility for
    top n candidates.
    :rtype: tuple
    """
    # Gain, based on original vote (utility) and elected candidate
    # Given a particular vote structure (ranking), return its utility
    # knowing the elected candidate
    num_candidates = len(vote)
    utility_increments = [(num_candidates - i) / (num_candidates * 1.0) for i in
                          range(num_candidates)]
    my_best = vote[0]  # utility for the top only
    utility_for_top = utility_increments[elected.index(my_best)]
    # Utility for my top n candidate
    total_utility = 0.0
    for i in range(topn):
        total_utility += utility_increments[elected.index(vote[i])]
    return utility_for_top, total_utility


def get_rule_utility(profile: Profile,
                     rule: Callable[[int], int | float],
                     topn: int,
                     verbose=False):
    """
    Calculates the total utility and "top n" utility for a given rule.

    :param profile: The voting profile.
    :type profile: Profile
    :param rule: The voting rule function.
    :type rule: Callable[[int], int | float]
    :param topn: The number of top candidates to consider for utility calculation.
    :type topn: int
    :param verbose: Print additional information if True, defaults to False.
    :type verbose: bool, optional
    :return: A dictionary containing the total utility for the top candidate and the total
    utility for top n candidates.
    :rtype: dict[str, float]
    """
    rule_name = rule.__name__
    ranking = profile.ranking(rule)
    elected_candidates = [c[0] for c in ranking]
    if verbose:
        print(f"Ranking based on '{rule_name}' gives {ranking} with winners {elected_candidates}")
        print("======================================================================")
    total_u, total_u_n = 0., 0.
    if verbose:
        print("Counts \t Ballot \t Utility of first")
    for pair in profile.pairs:
        # Utility of the ballot given elected_candidates, multipled by its counts
        u, u_n = voter_subjective_utility_for_elected_candidate(elected_candidates, pair[1],
                                                                topn=topn)
        if verbose:
            print(f"{pair[0]} \t {pair[1]} \t {u}")
        total_u += pair[0] * u
        total_u_n += pair[0] * u_n
    if verbose:
        print("Total : ", total_u)

    return {"top": total_u, "topn": total_u_n}


def evaluate_voting_rules(num_candidates: int,
                          num_voters: int,
                          topn: int,
                          voters_model: str,
                          verbose: bool = False
                          ) -> dict[str, dict[str, float]]:
    """
    Evaluates various voting rules and returns a dictionary with the results.

    :param num_candidates: The number of candidates.
    :type num_candidates: int
    :param num_voters: The number of voters.
    :type num_voters: int
    :param topn: The number of top candidates to consider for utility calculation.
    :type topn: int
    :param voters_model: The model used to generate the voter profiles.
    :type voters_model: str
    :param verbose: Print additional information if True, defaults to False.
    :type verbose: bool, optional
    :return: A dictionary containing the results for each voting rule.
    :rtype: dict[str, dict[str, float]]
    """
    profile = get_profile_from_model(num_candidates, num_voters, voters_model)

    rules = [borda_rule, copeland_rule, dowdall_rule, simpson_rule]
    # Adding some extra Borda variants, with decay parameter
    borda_variants = [get_borda_gamma(gamma) for gamma in
                      [1.0, 0.99, 0.75, 0.6, 0.25, 0.01]]
    rules.extend(borda_variants)

    result = {}
    for rule in rules:
        result[rule.__name__] = get_rule_utility(profile, rule, topn, verbose)
    return result
