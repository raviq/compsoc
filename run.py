"""
Entry point of the voting tournament.

Rafik Hadfi <rafik.hadfi@gmail.com>
"""

import argparse
import importlib
import inspect
import re

from tqdm import trange

from compsoc.utils import plot_final_results
from compsoc.evaluate import evaluate_voting_rules


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
        results[i] = evaluate_voting_rules(args.num_candidates, args.num_voters, args.num_topn,
                                           args.voters_model)
    plot_final_results(args.voters_model, results, args.num_voters, args.num_candidates,
                       args.num_topn, args.num_iterations)


if __name__ == "__main__":
    main()
