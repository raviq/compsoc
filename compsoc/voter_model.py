"""
Voter models
Definition of the ballots of the voters according to different generative models.
Results are probabilistic distributions over votes.
"""

import random
import numpy as np
import scipy.stats as ss
import matplotlib.pylab as plt
from pprint import pprint
from itertools import permutations
from collections import Counter
from matplotlib.ticker import MaxNLocator
from typing import List, Tuple, Optional

from compsoc.profile import Profile
from compsoc.utils import int_list_to_str


def generate_random_votes(number_voters: int,
                          number_candidates: int) -> List[Tuple[int, Tuple[int, ...]]]:
    candidate_list = list(range(number_candidates))
    votes = [random.sample(candidate_list, number_candidates) for vi in range(number_voters)]
    vote_strs = [int_list_to_str(vote) for vote in votes]
    vote_counts = Counter(vote_strs)
    ballots = [(count, tuple(map(int, vote.split(',')))) for vote, count in vote_counts.items()]
    return ballots


def generate_gaussian_votes(mu: float,
                            stdv: float,
                            num_voters: int,
                            num_candidates: int,
                            plot_save: Optional[bool] = True) -> List[Tuple[int, Tuple[int, ...]]]:
    # Gaussian generation of votes over candidates
    ballot_permutations = list(permutations(range(num_candidates)))
    x = np.arange(-len(ballot_permutations) / 2., len(ballot_permutations) / 2.)
    x_u, x_l = x + mu, x - mu
    prob = ss.norm.cdf(x_u, scale=stdv) - ss.norm.cdf(x_l, scale=stdv)  # scale specifies stdev
    prob /= prob.sum()
    dist = num_voters * prob
    dist = np.array(list(map(int, dist)))
    # Remove rankings with 0 occurence
    ballots = [(int(dist[i]), tuple(ballot_permutations[i])) for i, _ in enumerate(x) if dist[i]]
    if plot_save:
        _, ax = plt.subplots()
        dist_non_null_index = np.array([i for i, x in enumerate(dist) if x])
        plt.plot(x[dist_non_null_index], dist[dist_non_null_index], 'b.-', lw=0.4)
        plt.grid(color='gray', linestyle='dashed', linewidth=0.1)
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), rotation=90, fontsize=5)
        plt.xlabel('Votes')
        plt.ylabel('Number of occurences')
        ax.set_xticklabels(map(int_list_to_str, ballot_permutations))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title(rf'{num_voters} voters, {num_candidates} candidates, $\mu={mu}, $\sigma={stdv}$')
        plt.savefig('figures/Votes_gaussian_distribution.png', format='png', dpi=500)
    return ballots


def generate_multinomial_dirichlet_votes(alpha: List[float],
                                         num_voters: int,
                                         num_candidates: int) -> List[Tuple[int, Tuple[int, ...]]]:
    # Dirichlet Multinomial generation of votes over candidates
    candidates = list(range(1, num_candidates + 1))
    p = np.random.dirichlet(alpha, size=1).tolist()[0]
    votes = []
    for _ in range(num_voters):
        vote = np.random.choice(candidates, size=num_candidates, replace=False, p=p)
        vote = list(vote)
        votes.append(vote)
    ballots = []
    tmp = {}
    for vote in votes:
        vote_tuple = tuple(vote)
        if vote_tuple not in tmp:
            count = votes.count(vote)
            tmp[vote_tuple] = count
            ballots.append((count, list(vote_tuple)))
    return ballots


def test_gaussian():
    num_voters = 1000
    num_candidates = 4
    mu, stdv = 3, 10
    ballots = generate_gaussian_votes(mu, stdv, num_voters, num_candidates)
    pprint(ballots)


def test_dirichlet():
    num_voters = 20
    alpha_candidates = (1.1, 2.5, 3.8)
    num_candidates = len(alpha_candidates)
    ballots = generate_multinomial_dirichlet_votes(alpha_candidates, num_voters, num_candidates)
    pprint(ballots)


def get_profile_from_model(num_candidates, num_voters, voters_model, verbose=False) -> Profile:
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

    if verbose:
        print(profile)

    return profile
