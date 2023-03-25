import unittest
from compsoc.profile import Profile
from compsoc.voting_rules.borda import borda_rule


class TestProfile(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            (17, (1, 3, 2, 0)),
            (40, (3, 0, 1, 2)),
            (52, (1, 0, 2, 3)),
            (20, (0, 1, 2, 3)),
        }
        self.profile = Profile(self.test_data)

    def test_init(self):
        self.assertEqual(self.profile.pairs, self.test_data)
        self.assertEqual(self.profile.candidates, {0, 1, 2, 3})
        self.assertEqual(self.profile.total_votes, 129)

    def test_get_net_preference(self):
        self.assertEqual(self.profile.get_net_preference(1, 3), 49)
        self.assertEqual(self.profile.get_net_preference(1, 2), 129)
        self.assertEqual(self.profile.get_net_preference(0, 2), 95)

    def test_does_pareto_dominate(self):
        self.assertTrue(self.profile.does_pareto_dominate(1, 2))
        self.assertFalse(self.profile.does_pareto_dominate(0, 2))

    def test_score(self):
        test_rule = borda_rule
        expected_score = [(0, 244), (1, 287), (2, 89), (3, 154)]
        self.assertEqual(self.profile.score(test_rule), expected_score)

    def test_ranking(self):
        test_rule = borda_rule
        expected_ranking = [(1, 287), (0, 244), (3, 154), (2, 89)]
        self.assertEqual(self.profile.ranking(test_rule), expected_ranking)

    def test_winners(self):
        test_rule = borda_rule
        expected_winners = {1}
        self.assertEqual(self.profile.winners(test_rule), expected_winners)

    def test_parse_voting_data(self):
        # TODO: Implement this test.
        pass

    def test_ballot_box(self):
        choices = [
            (3, 2, 1, 0),
            (1, 0, 2, 3),
            (1, 0, 2, 3),
        ]
        profile = Profile.ballot_box(choices)
        self.assertEqual(profile.pairs, {(2, (1, 0, 2, 3)), (1, (3, 2, 1, 0))})
        self.assertEqual(profile.candidates, {0, 1, 2, 3})
        self.assertEqual(profile.total_votes, 3)


if __name__ == "__main__":
    unittest.main()
