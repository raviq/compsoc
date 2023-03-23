import unittest
from itertools import permutations
from typing import List, Tuple

from compsoc.voter_model import (
    generate_random_votes,
    generate_gaussian_votes,
    generate_multinomial_dirichlet_votes,
    get_pairs_from_model,
)


# Helper function to validate generated ballots
def validate_ballots(ballots: List[Tuple[int, Tuple[int, ...]]], num_voters: int,
                     num_candidates: int) -> bool:
    total_voters = sum([count for count, _ in ballots])
    unique_votes = set([vote for _, vote in ballots])
    all_permutations = set(permutations(range(num_candidates)))
    return total_voters == num_voters and unique_votes.issubset(all_permutations)


class TestVoterModel(unittest.TestCase):
    def test_generate_random_votes(self):
        num_voters = 100
        num_candidates = 4
        ballots = generate_random_votes(num_voters, num_candidates)
        self.assertTrue(validate_ballots(ballots, num_voters, num_candidates))

    def test_generate_gaussian_votes(self):
        num_voters = 100
        num_candidates = 4
        mu, stdv = 2, 1
        ballots = generate_gaussian_votes(mu, stdv, num_voters, num_candidates, plot_save=False)
        self.assertTrue(validate_ballots(ballots, num_voters, num_candidates))

    def test_generate_multinomial_dirichlet_votes(self):
        num_voters = 100
        alpha_candidates = (1.1, 2.5, 3.8)
        num_candidates = len(alpha_candidates)
        ballots = generate_multinomial_dirichlet_votes(alpha_candidates, num_voters, num_candidates)
        self.assertTrue(validate_ballots(ballots, num_voters, num_candidates))

    def test_get_pairs_from_model(self):
        num_voters = 100
        num_candidates = 4
        for model in ["random", "gaussian", "multinomial_dirichlet"]:
            pairs = get_pairs_from_model(num_candidates, num_voters, model)
            self.assertTrue(validate_ballots(pairs, num_voters, num_candidates))


if __name__ == "__main__":
    unittest.main()
