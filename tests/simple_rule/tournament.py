"""
Standalone evaluation of one voting rule against baselins rules
Python 3.9
"""

import re
import argparse
import importlib
import inspect
from tqdm import trange
from typing import List, Tuple, Callable, Set

from compsoc.profile import Profile
from compsoc.voter_model import get_profile_from_model
from compsoc.voting_rules.borda import borda_rule
from compsoc.voting_rules.borda_gamma import get_borda_gamma
from compsoc.voting_rules.copeland import copeland_rule
from compsoc.voting_rules.dowdall import dowdall_rule
from compsoc.voting_rules.simpson import simpson_rule
from compsoc.evaluate import get_rule_utility,voter_subjective_utility_for_elected_candidate
from compsoc.plot import plot_comparison_results

# Your rule is implemented here:
from borda_alpha import get_borda_alpha

def evaluate_my_voting_rule(num_candidates: int,
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
    borda_rule.__name__ = "Borda"
    copeland_rule.__name__ = "Copeland"
    dowdall_rule.__name__ = "Dowdall"
    simpson_rule.__name__ = "Simpson"

    #----------------------------------------------------------------
    # Rules to test against
    #----------------------------------------------------------------
    # Adding classic rules
    rules = [borda_rule, copeland_rule, dowdall_rule, simpson_rule]
    # Adding some extra Borda variants, with decay parameter
    for gamma in [1.0, 0.8, 0.6, 0.4]:
        gamma_rule = get_borda_gamma(gamma)
        gamma_rule.__name__ = f"Borda $\\gamma$({gamma})"
        rules.append(gamma_rule)

    #----------------------------------------------------------------
    # Finally, adding your rule, example, similar to Borda gamma.
    #----------------------------------------------------------------`
    for alpha in [0.3, 0.2, 0.1]:
        alpha_rule = get_borda_alpha(alpha)
        alpha_rule.__name__ = f"Borda $\\alpha$({alpha})"
        rules.append(alpha_rule)

    # Get results
    result = {}
    for rule in rules:
        result[rule.__name__] = get_rule_utility(profile, rule, topn, verbose)
    return result

def main():
    # Import voter models names from models.py.
    # Each must be implemented as 'generate_M_votes'
    voter_model_folder = "compsoc.voter_model"
    module = importlib.import_module(voter_model_folder)
    functions = inspect.getmembers(module, inspect.isfunction)
    voters_model_distributions = []
    for function in functions:
        match = re.search(r"generate_(.*)_votes", function[0])
        if match:
            voters_model_distributions.append(match.group(1))
    if not voters_model_distributions:
        raise Exception(f"No voter models found in {voter_model_folder}.")
    
    # Loading arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("num_candidates", type=int, help="Number of candidates")
    parser.add_argument("num_voters", type=int, help="Number of voters")
    parser.add_argument("num_iterations", type=int, help="Number of iterations")
    parser.add_argument("num_topn", type=int, help="Top N.")
    parser.add_argument("voters_model", type=str,
                        choices=voters_model_distributions,
                        help=f"Model for the generation of voters: "
                             f"{', '.join(voters_model_distributions)}")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Increases output verbosity")
    args = parser.parse_args()
    # Results
    results = {}
    for i in trange(args.num_iterations):
        results[i] = evaluate_my_voting_rule(   args.num_candidates,
                                                args.num_voters,
                                                args.num_topn,
                                                args.voters_model,
                                           verbose=True)
    plot_comparison_results(args.voters_model, results, args.num_voters, args.num_candidates,
                            args.num_topn, args.num_iterations, save_figure=True)


if __name__ == "__main__":
    main()
