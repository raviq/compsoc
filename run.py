"""
Entry point of the voting tournament.
Rafik Hadfi <rafik.hadfi@gmail.com>
"""

import random
import re
import argparse
from tqdm import trange
from profile import Profile
from models import *
from utils import *

def voter_subjective_utility_for_elected_candidate(elected, vote):
    # Gain, based on original vote (utility) and elected candidate
    # Given a particular vote structure (ranking), return its utility knowing the elected candidate
    num_candidates = len(vote)
    utility_increments = [(num_candidates - _)/ (1. * num_candidates) for _ in range(num_candidates)]
    # utility for the top only
    my_best = vote[0]
    u = utility_increments[elected.index(my_best)]
    # Utility for my top n candidate
    n = 2
    U = 0.
    for i in range(n):
        U += utility_increments[elected.index(vote[i])]
    return u, U

def evaluate_voting_rules(num_candidates, num_voters, voters_model="random", verbose=False):
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
        ballots = generate_random_votes(num_voters, num_candidates)

    # Setting up the profile with the generated ballots
    profile = Profile(ballots)
    profile.show()

    # Setting up voting rules. All are rankings.
    rules = [   profile.dowdall,
                profile.simpson,
                profile.copeland,
                profile.borda,
                #profile.my_new_borda
            ]
    # Generating results
    result = {}
    for rule in rules:
        rule_name = re.search('Profile\.(.*)\ of', str(rule)).group(1)
        ranking = profile.ranking(rule)
        elected_candidates = list(map(lambda x: x[0], ranking))

        print ("Ranking based on '{}' gives {} with winners {}".format(rule_name, ranking, elected_candidates))
        print ("=====================================================================================")

        U, Un = 0., 0.
        print ("Counts \t Ballot \t Utility of first")
        for counts, ballot in profile.pairs:
            # Utility of the ballot given elected_candidates, multipled by its counts
            u, un = voter_subjective_utility_for_elected_candidate(elected_candidates, ballot)
            print ("%s \t %s \t %s" % (counts, ballot, u))
            U += counts * u
            Un += counts * un
        print ("Total : ", U)
        result[rule.__name__] = {'top' : U, 'topn' : Un}
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("num_candidates", type=int, help="Number of candidates")
    parser.add_argument("num_voters", type=int, help="Number of voters")
    parser.add_argument("num_iterations", type=int, help="Number of iterations")
    parser.add_argument("voters_model", type=str, help="Model for the generation of voters, either \"random\" or \"multinomial_dirichlet\"")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increases output verbosity")
    args = parser.parse_args()

    results = {}
    for i in trange(args.num_iterations):
        results[i] = evaluate_voting_rules(args.num_candidates, args.num_voters, args.voters_model)
    plot_final_results(args.voters_model, results, args.num_voters, args.num_candidates, args.num_iterations)

if __name__ == "__main__":
    main()
