"""
python3.9 run.py 10 1000 10 1 0.1 random
"""

import argparse
import importlib
import inspect
import re

from tqdm import trange

from compsoc.plot import plot_comparison_results
from compsoc.evaluate import evaluate_voting_rules
from compsoc.voter_model import get_profile_from_model

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
    parser.add_argument("distortion_ratio", type=float, help="Distort ratio")
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
        results[i] = evaluate_voting_rules(args.num_candidates,
                                           args.num_voters,
                                           args.num_topn,
                                           args.voters_model,
                                           verbose=True)
    plot_comparison_results(args.voters_model, results, args.num_voters, args.num_candidates,
                            args.num_topn, args.num_iterations, distortion_ratio=0.0, save_figure=True)
    
    if args.distortion_ratio == 0.0:
        return

    results2 = {}
    for i in trange(args.num_iterations):
        results2[i] = evaluate_voting_rules(args.num_candidates,
                                           args.num_voters,
                                           args.num_topn,
                                           args.voters_model,
                                           distortion_ratio=args.distortion_ratio,
                                           verbose=True)
    plot_comparison_results(args.voters_model, results2, args.num_voters, args.num_candidates,
                            args.num_topn, args.num_iterations, distortion_ratio=args.distortion_ratio, save_figure=True)


if __name__ == "__main__":
    p = get_profile_from_model(num_candidates=10, num_voters=00, voters_model='gaussian', verbose=False)
    print (p)