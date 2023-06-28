import unittest
from compsoc.profile import Profile
from compsoc.voting_rules.borda import borda_rule


class TestDistortedProfile(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            (17, (1, 3, 2, 0)),
            (40, (3, 0, 1, 2)),
            (52, (1, 0, 2, 3)),
            (20, (0, 1, 2, 3)),
        }
        self.profile = Profile(self.test_data)

    def test_0_distortion(self):
        """
        No distortion
        """
        self.profile.distort(0.0)
        self.assertEqual(self.profile.pairs, self.test_data)

    def test_0_5_distortion(self):
        """
        All ballots are cut in half
        """
        self.profile.distort(0.5)
        self.assertNotEqual(self.profile.pairs, self.test_data)
        self.assertEqual(self.profile.pairs, {
            (17, (1, 3)),
            (40, (3, 0)),
            (52, (1, 0)),
            (20, (0, 1)),
        })

    def test_1_distortion(self):
        """
        Only the first candidate is left
        """
        self.profile.distort(1)
        self.assertNotEqual(self.profile.pairs, self.test_data)
        self.assertEqual(self.profile.pairs, {
            (40, (3,)),
            (69, (1,)),
            (20, (0,)),
        })

    def test_get_net_preference(self):
        """
        Test net preference
        """
        self.profile.distort(0.5)
        self.assertEqual(self.profile.get_net_preference(1, 3), 17)
        self.assertEqual(self.profile.get_net_preference(3, 0), 40)
        # If one of the candidates are missing in the ballot, the net preference is 0
        self.assertEqual(self.profile.get_net_preference(0, 2), 0)
        self.assertEqual(self.profile.get_net_preference(3, 2), 0)

    def test_does_pareto_dominate(self):
        """
        Test pareto
        """
        self.profile.distort(0.5)
        self.assertTrue(self.profile.does_pareto_dominate(1, 2))
        self.assertFalse(self.profile.does_pareto_dominate(0, 1))

    def test_score(self):
        """
        Test score
        """
        self.profile.distort(0.5)
        test_rule = borda_rule
        expected_score = [(0, 244), (1, 247), (2, 0), (3, 154)]
        self.assertEqual(self.profile.score(test_rule), expected_score)

    def test_ranking(self):
        """
        Test ranking

        """
        self.profile.distort(0.5)
        test_rule = borda_rule
        expected_ranking = [(1, 247), (0, 244), (3, 154), (2, 0)]
        self.assertEqual(self.profile.ranking(test_rule), expected_ranking)

    def test_winners(self):
        self.profile.distort(0.5)
        test_rule = borda_rule
        expected_winners = {1}
        self.assertEqual(self.profile.winners(test_rule), expected_winners)


if __name__ == "__main__":
    unittest.main()
