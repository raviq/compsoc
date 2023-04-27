import unittest

from compsoc.profile import Profile
from compsoc.voting_rules.borda import borda_rule
from compsoc.voting_rules.copeland import copeland_rule
from compsoc.evaluate import get_rule_utility


class TestRules(unittest.TestCase):

    def setUp(self):
        self.profile = Profile({
            (3, (0, 1, 2)),
            (2, (1, 0, 2)),
            (1, (2, 0, 1))
        })

    def test_borda_rule(self):
        borda_scores = [
            borda_rule(self.profile, 0),
            borda_rule(self.profile, 1),
            borda_rule(self.profile, 2)
        ]
        self.assertEqual(borda_scores, [9, 7, 2])

        utility = get_rule_utility(self.profile, borda_rule, 1)
        self.assertEqual(utility, {'top': 4.666666666666666, 'topn': 4.666666666666666})

    def test_copeland_rule(self):
        copeland_scores = [
            copeland_rule(self.profile, 0),
            copeland_rule(self.profile, 1),
            copeland_rule(self.profile, 2)
        ]
        self.assertEqual(copeland_scores, [2, 0, -2])


if __name__ == "__main__":
    unittest.main()
