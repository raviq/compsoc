"""
Test the voter model functions.
"""
import unittest
from itertools import permutations
from typing import List, Tuple

from compsoc.voter_model import (
    generate_gaussian_votes, generate_multinomial_dirichlet_votes, generate_random_votes, get_pairs_from_model)


# Helper function to validate generated ballots
def validate_ballots(ballots: List[Tuple[int, Tuple[int, ...]]], num_voters: int,
                     num_candidates: int) -> bool:
    total_voters = sum(count for count, _ in ballots)
    unique_votes = set(vote for _, vote in ballots)
    all_permutations = set(permutations(range(num_candidates)))
    return total_voters == num_voters and unique_votes.issubset(all_permutations)


class TestVoterModel(unittest.TestCase):
    """
    Test the voter model functions.
    """

    def test_generate_random_votes(self):
        num_voters = 100
        num_candidates = 4
        ballots = generate_random_votes(num_voters, num_candidates)
        self.assertTrue(validate_ballots(ballots, num_voters, num_candidates))

    def test_generate_gaussian_votes(self):
        """
        Test the Gaussian voter model with a known distribution.
        """
        num_voters = 100
        num_candidates = 4
        mu, stdv = 2, 1
        expected_ballots = [(3, (1, 2, 3, 0)), (12, (1, 3, 0, 2)), (20, (1, 3, 2, 0)),
                            (30, (2, 0, 1, 3)), (20, (2, 0, 3, 1)), (12, (2, 1, 0, 3)),
                            (3, (2, 1, 3, 0))]
        ballots = generate_gaussian_votes(mu, stdv, num_voters, num_candidates, plot_save=False)
        self.assertEqual(ballots, expected_ballots)
        self.assertTrue(validate_ballots(ballots, num_voters, num_candidates))

    def test_generate_multinomial_dirichlet_votes(self):
        """
        Test the Multinomial Dirichlet voter model with a known distribution.
        """
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

    def test_gaussian_votes_mu_stdv(self):
        """
        Test if mu and stdv kwargs affect the distribution of the Gaussian model.
        """
        num_voters = 1000
        num_candidates = 4
        mu, stdv = 2, 1

        ballots_default = get_pairs_from_model(num_candidates, num_voters, "gaussian")
        ballots_high_mu = get_pairs_from_model(num_candidates, num_voters, "gaussian", mu=mu + 1, stdv=stdv)

        # Validate ballots
        self.assertTrue(validate_ballots(ballots_default, num_voters, num_candidates))
        self.assertTrue(validate_ballots(ballots_high_mu, num_voters, num_candidates))

        self.assertTrue(ballots_default != ballots_high_mu)

    def test_multinomial_dirichlet_votes_alpha(self):
        """
        Test if alpha_low and alpha_high kwargs affect the distribution of the Multinomial Dirichlet model.
        """
        num_voters = 1000
        num_candidates = 4
        alpha_low, alpha_high = 2, 3

        ballots_default = get_pairs_from_model(num_candidates, num_voters, 'multinomial_dirichlet')
        ballots_high_alpha = get_pairs_from_model(num_candidates, num_voters, 'multinomial_dirichlet', alpha_low=alpha_high, alpha_high=alpha_high)

        self.assertTrue(ballots_default != ballots_high_alpha)


if __name__ == "__main__":
    unittest.main()
