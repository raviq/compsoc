from typing import List, Tuple, Any, Callable

from compsoc.profile import Profile
from compsoc.voter_model import generate_gaussian_votes, generate_multinomial_dirichlet_votes, \
    generate_random_votes
from compsoc.voting_rules.borda import borda_rule
from compsoc.voting_rules.borda_gamma import get_borda_gamma
from compsoc.voting_rules.copeland import copeland_rule
from compsoc.voting_rules.dowdall import dowdall_rule
from compsoc.voting_rules.simpson import simpson_rule


def load_voter_model(num_candidates, num_voters, voters_model) -> Profile:
    # Generating the ballots acsoring to some model
    if voters_model == "multinomial_dirichlet":
        # Random alphas might cause precision problems with the generation of P, when values are
        # small
        #   tuple(np.random.rand(1, num_candidates)[0])
        # Instead, the population hyperparam should be set according the competition goals.
        alpha = (1.1, 2.5, 3.8, 2.1, 1.3)
        pairs = generate_multinomial_dirichlet_votes(alpha, num_voters, num_candidates)
    elif voters_model == "gaussian":
        mu, stdv = 2, 1  # Depends on 'num_voters'
        pairs = generate_gaussian_votes(mu, stdv, num_voters, num_candidates)
    elif voters_model == "random":
        pairs = generate_random_votes(num_voters, num_candidates)
    else:
        # Default
        pairs = generate_random_votes(num_voters, num_candidates)
    # Setting up the profile with the generated ballots
    profile = Profile(pairs)
    print(profile)

    return profile


def voter_subjective_utility_for_elected_candidate(elected: List[int], vote: Tuple[int],
                                                   topn: int) -> tuple:
    # Gain, based on original vote (utility) and elected candidate
    # Given a particular vote structure (ranking), return its utility knowing the elected candidate
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
    Get the total utility and "top n" utility for a given rule,
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
            print("%s \t %s \t %s" % (pair[0], pair[1], u))
        total_u += pair[0] * u
        total_u_n += pair[0] * u_n
    if verbose:
        print("Total : ", total_u)

    return {"top": total_u, "topn": total_u_n}


def evaluate_voting_rules(num_candidates,
                          num_voters,
                          topn,
                          voters_model,
                          verbose: bool = False
                          ) -> dict[str, dict[str, float]]:
    #######################
    # Loading the profile #
    #######################

    profile = load_voter_model(num_candidates, num_voters, voters_model)

    ########################
    # Generating the rules #
    ########################

    rules = [borda_rule, copeland_rule, dowdall_rule, simpson_rule]
    # Adding some extra Borda variants, with decay parameter
    borda_variants = [get_borda_gamma(gamma) for gamma in
                      [1.0, 0.99, 0.75, 0.6, 0.25, 0.01]]
    rules.extend(borda_variants)

    #######################
    # Generating results  #
    #######################

    result = {}
    for rule in rules:
        result[rule.__name__] = get_rule_utility(profile, rule, topn, verbose)
    return result
