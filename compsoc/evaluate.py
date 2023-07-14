"""
Evaluation functions
"""
from typing import List, Tuple, Callable

from itertools import permutations

from compsoc.profile import Profile
from compsoc.voter_model import get_profile_from_model, generate_distorted_from_normal_profile
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
    :return: A tuple containing utility for the top candidate and total utility for top n candidates.
    :rtype: tuple
    """
    # Gain, based on original vote (utility) and elected candidate
    # Given a particular vote structure (ranking), return its utility
    # knowing the elected candidate
    num_candidates = len(elected)
    utility_increments = [(num_candidates - i) / (num_candidates * 1.0) for i in range(num_candidates)]
    
    my_best = vote[0]  # utility for the top only
    utility_for_top = utility_increments[elected.index(my_best)]
    # Utility for my top n candidate
    total_utility = 0.0
    for i in range(min(topn, len(vote))):
        total_utility += utility_increments[elected.index(vote[i])]
    return utility_for_top, total_utility


def get_rule_utility(profile: Profile,
                     rule: Callable[[Profile, int], any],
                     topn: int,
                     verbose=True):
    """
    Calculates the total utility and "top n" utility for a given rule.

    :param profile: The voting profile.
    :type profile: Profile
    :param rule: The voting rule function.
    :type rule: Callable[[int], int],# | float],
    :param topn: The number of top candidates to consider for utility calculation.
    :type topn: int
    :param verbose: Print additional information if True, defaults to False.
    :type verbose: bool, optional
    :return: A dictionary containing the total utility for the top candidate and the total utility for top n candidates.
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
                          distortion_rate: float = 0.0,
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
    :param distortion_rate: The distortion rate, defaults to 0.0.
    :type distortion_rate: int, optional
    :param verbose: Print additional information if True, defaults to False.
    :type verbose: bool, optional
    :return: A dictionary containing the results for each voting rule.
    :rtype: dict[str, dict[str, float]]

    """
    profile = get_profile_from_model(num_candidates, num_voters, voters_model)
    profile.distort(distortion_rate)
    if verbose:
        print(profile.pairs)
    borda_rule.__name__ = "Borda"
    copeland_rule.__name__ = "Copeland"
    dowdall_rule.__name__ = "Dowdall"
    simpson_rule.__name__ = "Simpson"

    rules = [borda_rule, copeland_rule, dowdall_rule, simpson_rule]
    # Adding some extra Borda variants, with decay parameter
    for gamma in [1.0, 0.99, 0.75, 0.6, 0.25, 0.01]:
        gamma_rule = get_borda_gamma(gamma)
        gamma_rule.__name__ = f"Borda Gamma({gamma})"
        rules.append(gamma_rule)

    result = {}
    for rule in rules:
        result[rule.__name__] = get_rule_utility(profile, rule, topn, verbose)
    return result

def get_rule_utility_normalized(profile: Profile, rule: Callable[[Profile, int], any], topn: int, verbose=False):
    utility = get_rule_utility(profile, rule, topn, verbose)
    top1u = utility['top']; topnu = utility['topn']
    num_vote = profile.total_votes
    num_candidate = len(profile.candidates)
    norm_top1u = (top1u / num_vote) * 100.0
    utility_increments = [(num_candidate - i) / (num_candidate * 1.0) for i in range(num_candidate)]
    norm_factor = max(topn, len(list(profile.pairs)[0][1])) / sum(utility_increments[0:max(topn, len(list(profile.pairs)[0][1]))])
    norm_topnu = (((topnu / num_vote) * 100.0) * norm_factor) / max(topn, len(list(profile.pairs)[0][1]))
    return {"top": norm_top1u, "topn": norm_topnu}

def get_rule_utility_normalized2(profile: Profile, rule: Callable[[Profile, int], any], topn: int, verbose=False):
    borda_utility = get_rule_utility(profile, borda_rule, topn, verbose)
    utility = get_rule_utility(profile, rule, topn, verbose)
    top = 100 * utility['top']/borda_utility['top']
    topn = 100 * utility['topn']/borda_utility['topn']

    return {"top": top, "topn": topn}
    


'''
def get_rule_utility_normalized(profile: Profile, rule: Callable[[Profile, int], any], topn: int):
    rule_name = rule.__name__
    ranking = profile.ranking(rule)

    elected_candidates = [c[0] for c in ranking]

    total_u, total_u_n = 0., 0.
    for pair in profile.pairs:

        u, u_n = voter_subjective_utility_for_elected_candidate(elected_candidates, pair[1], topn=topn)

        total_u += pair[0] * u
        total_u_n += pair[0] * u_n

    max_total_u = total_u
    max_total_u_n = total_u_n
    min_total_u = total_u
    min_total_u_n = total_u_n

    candidates = list(range(len(profile.candidates)))
    permu_list = list(permutations(candidates))

    for i in permu_list:
        t = list(i)
        ttotal_u, ttotal_u_n = 0., 0.

        for pair in profile.pairs:

            u, u_n = voter_subjective_utility_for_elected_candidate(t, pair[1], topn=topn)
            ttotal_u += pair[0] * u
            ttotal_u_n += pair[0] * u_n
        
        if ttotal_u > max_total_u:
            max_total_u = ttotal_u
        if ttotal_u_n > max_total_u_n:
            max_total_u_n = ttotal_u_n
        if ttotal_u < min_total_u:
            min_total_u = ttotal_u
        if ttotal_u_n < min_total_u_n:
            min_total_u_n = ttotal_u_n
    
    total_u = ((total_u - min_total_u)/(max_total_u - min_total_u))*200.0 - 100
    total_u_n = ((total_u_n - min_total_u_n)/(max_total_u_n - min_total_u_n))*200.0 - 100
    return {"top": total_u, "topn": total_u_n}

'''

