"""
Entry point of the voting tournament.

Rafik Hadfi <rafik.hadfi@gmail.com>
"""

import re
import argparse
import importlib
import inspect
from tqdm import trange
from typing import List
from profile import Profile
from utils import *
from voter_model import *
from voting_rules import *

def voter_subjective_utility_for_elected_candidate(elected: List[int], vote: List[int], topn: int) -> tuple:
    # Gain, based on original vote (utility) and elected candidate
    # Given a particular vote structure (ranking), return its utility knowing the elected candidate
    num_candidates = len(vote)
    utility_increments = [(num_candidates - i)/ (num_candidates * 1.0) for i in range(num_candidates)]
    my_best = vote[0] # utility for the top only
    utility_for_top = utility_increments[elected.index(my_best)]
    # Utility for my top n candidate
    total_utility = 0.0
    for i in range(topn):
        total_utility += utility_increments[elected.index(vote[i])]
    return utility_for_top, total_utility

def evaluate_voting_rules(num_candidates, num_voters, topn, voters_model, verbose=False):
    #######################################################################
    ## Loading voter models
    #######################################################################

    # Generating the ballots acsoring to some model
    if voters_model == "multinomial_dirichlet":
        # Random alphas might cause precision problems with the generation of P, when values are small
        #   tuple(np.random.rand(1, num_candidates)[0])
        # Instead, the population hyperparam should be set according the competition goals.
        alpha = (1.1, 2.5, 3.8, 2.1, 1.3)
        ballots = generate_multinomial_dirichlet_votes(alpha, num_voters, num_candidates)
    elif voters_model == "gaussian":
        mu, stdv = 2, 1 # Depends on 'num_voters'
        ballots = generate_gaussian_votes(mu, stdv, num_voters, num_candidates)
    elif voters_model == "random":
        ballots = generate_random_votes(num_voters, num_candidates)
    else:
        # Default
        ballots = generate_random_votes(num_voters, num_candidates)
    # Setting up the profile with the generated ballots
    profile = Profile(ballots)
    profile.show()
    #######################################################################
    ## Loading voting rules
    #######################################################################
    rules = [   dowdall.create_rule(profile),
                simpson.create_rule(profile),
                copeland.create_rule(profile),
                borda.create_rule(profile)
            ]
    # Adding some extra Borda variants, with decay parameter
    borda_variants = [borda_gamma.create_rule(profile, gamma)
                        for gamma in [1.0, 0.99, 0.75, 0.6, 0.25, 0.01]]
    rules.extend(borda_variants)

    #######################################################################
    ## Generating results
    #######################################################################
    result = {}
    for rule in rules:
        rule_name = rule.__name__
        ranking = profile.ranking(rule)
        elected_candidates =  [c[0] for c in ranking]
        print ("Ranking based on '{}' gives {} with winners {}".format(rule_name, ranking, elected_candidates))
        print ("======================================================================")
        U, Un = 0., 0.
        print ("Counts \t Ballot \t Utility of first")
        for counts, ballot in profile.pairs:
            # Utility of the ballot given elected_candidates, multipled by its counts
            u, un = voter_subjective_utility_for_elected_candidate(elected_candidates, ballot, topn=topn)
            print ("%s \t %s \t %s" % (counts, ballot, u))
            U += counts * u
            Un += counts * un
        print ("Total : ", U)
        result[rule.__name__] = {'top' : U, 'topn' : Un}
    return result

def main():
    try:
        # Import voter models names from models.py.
        # Each must be implemented as 'generate_M_votes'
        voter_model_folder = "voter_model"
        module = importlib.import_module(voter_model_folder)
        functions = inspect.getmembers(module, inspect.isfunction)
        voters_model_distributions = []
        for function in functions:
            match = re.search(r'generate_(.*)_votes', function[0])
            if match:
                voters_model_distributions.append(match.group(1))
        if not voters_model_distributions:
            raise Exception("No voter models found in {}.".format(voter_model_folder))
        # Loading arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("num_candidates", type=int, help="Number of candidates")
        parser.add_argument("num_voters", type=int, help="Number of voters")
        parser.add_argument("num_iterations", type=int, help="Number of iterations")
        parser.add_argument("num_topn", type=int, help="Top N." )
        parser.add_argument("voters_model", type=str,
                                            choices=voters_model_distributions,
                                            help="Model for the generation of voters: {}".format(", ".join(voters_model_distributions)))
        parser.add_argument("-v", "--verbose", action="store_true", help="Increases output verbosity")
        args = parser.parse_args()
        # Results
        results = {}
        for i in trange(args.num_iterations):
            results[i] = evaluate_voting_rules(args.num_candidates, args.num_voters, args.num_topn, args.voters_model)
        plot_final_results(args.voters_model, results, args.num_voters, args.num_candidates, args.num_topn, args.num_iterations)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
