"""
Voting profiles
"""

import sys
from collections import Counter
from itertools import combinations
from typing import List, Tuple, Set

import numpy as np

sys.setrecursionlimit(1000000)


class Profile:
    """
    VotingProfile is a set of tuples, {(no. of occurences, ballot),...},
    wherein the ballot is defined as some ordering of the candidates.
    For instance:
        votes = Profile({(17, (1,3,2,0)), (40, (3,0,1,2)), (52, (1,0,2,3))})
    means 17 people like candidate 1 the most, then candidate 3 in the second
    position, then candidate 2 in the third position, and so on.

    Properties:
        pairs -- set of pairs e.g. (number of votes, ballot)
        candidates -- set of candidates in ballots
        total_votes -- total number of votes
        net_preference_graph -- represents the preference net
        votes_per_candidate -- total votes for each candidate
    """

    def __init__(self, pairs: Set[Tuple[int, Tuple[int, ...]]], num_candidates: None | int = None):
        self.pairs = pairs
        # num_candidates might be passed when a file with voting data is parsed
        # otherwise get candidates from ballot of first pair
        self.candidates = set(range(0, num_candidates)) if num_candidates \
            else set(list(pairs)[0][1])
        # Sum the frequencies of all the pairs
        self.total_votes = sum(pair[0] for pair in pairs)
        # Create a Net Preference Graph
        self.__calc_net_preference()
        # Set votes_per_candidate for Plurality
        self.__calc_votes_per_candidate()
        # Initialize a Path Preference Graph
        self.path_preference_graph = {candidate: {} for candidate in self.candidates}

    # ---------------------------------------------
    # Comparison routines
    # ---------------------------------------------
    def get_net_preference(self, candidate1, candidate2):
        """
        Computes preference between 2 candidates according to
        the Net Preference Graph and returns its answer
        Arguments:
        candidate1 -- candidate to be compared
        candidate2 -- other candidate to be compared
        """
        # Get the preference of candidate1 over candidate2
        return self.net_preference_graph[candidate1][candidate2]

    def does_pareto_dominate(self, candidate1, candidate2):
        """
        Returns True when candidate1 is preferred in all ballots.
        False, otherwise.
        :param candidate1: Candidate to be compared
        :param candidate2: Other candidate
        :return:
        """
        # A boolean list as candidate1 preferred
        preferred = [
            pair[1].index(candidate1) < pair[1].index(candidate2) for
            pair in
            self.pairs]
        # Apply AND on all elements in list
        return all(preferred)

    def score(self, scorer) -> List[tuple[int, float]]:
        """
        Returns a set of candidate scores according to some score function.
        Arguments:
        :param scorer: Score function (Borda, Copeland etc.)
        :return: a sorted list of (candidate, score)
        """
        scores = [(candidate, scorer(self, candidate)) for candidate in
                  self.candidates]

        # Sorted by candidate id in increasing order
        scores.sort(key=lambda x: x[0])

        return scores

    def ranking(self, scorer):
        """
        Returns a set of candidate winners according to some score function.
        :param scorer: The voting rule to use. (borda, copeland etc.)
        :return: List of tuples, e.g. [(1,111), (2,108), (0,78)]
        """
        # A list of (candidate, score)
        scores = self.score(scorer)
        scores.sort(key=lambda x: x[1], reverse=True)
        # Ranking is the score list ordered by score in descending order
        return scores

    def winners(self, scorer):
        """
        Returns a set of candidate winners according to some score function
        Arguments:
        scorer -- score function (ex.: borda, copeland)
        """
        ranking = self.ranking(scorer)  # get ranking
        best_score = ranking[0][1]  # get best score first tuple in ranking
        # Filter ranking to get all best score
        bests = list(filter(lambda x: x[1] == best_score, ranking))
        # Get only the candidates
        winners, _ = zip(*bests)
        # Return a set of winners
        return set(winners)

    @staticmethod
    def __preference(num_votes, candidate_1_index, candidate_2_index) -> int:
        """
        Computes the preference between 2 candidates and returns
        the preference according to the number of votes.
        :param num_votes: Number of votes
        :param candidate_1_index: Index of first candidate
        :param candidate_2_index: Index of second candidate
        :return: The preference value
        """
        n = candidate_1_index - candidate_2_index
        # Exception: if n is equal to 0, preference is 0,
        # otherwise preference is num_votes * sign(n)
        return 0 if n == 0 else num_votes * np.sign(n)

    def __calc_net_preference(self):
        """
        Create a Net Preference Graph.
        """
        candidates = list(self.candidates)
        num_candidates = len(candidates)
        self.net_preference_graph = {candidate: {} for candidate in candidates}
        for i in range(num_candidates):
            candidate_1 = candidates[i]
            for j in range(i, num_candidates):
                candidate_2 = candidates[j]
                # Preference list
                preferences = []
                # For each pair of voting data
                for freq, ballot in self.pairs:
                    # If both candidates are in the ballot
                    if candidate_1 in ballot and candidate_2 in ballot:
                        candidate_1_index = ballot.index(candidate_1)
                        candidate_2_index = ballot.index(candidate_2)

                        pref = self.__preference(freq,
                                                 candidate_2_index,
                                                 candidate_1_index)
                        preferences.append(pref)  # save preference
                # Computes the preference
                preference = sum(preferences)
                # Save preferences
                # candidate1 VS candidate2
                self.net_preference_graph[candidate_1][candidate_2] = preference
                # candidate2 VS candidate1
                self.net_preference_graph[candidate_2][candidate_1] = -preference

    def __calc_votes_per_candidate(self):
        """Computes total votes per each candidate for each rank position"""
        # Initialize structure to save the scores
        self.votes_per_candidate = []
        # Number of candidate
        n_candidates = len(self.candidates)
        # For each candidate
        for i in range(n_candidates):
            self.votes_per_candidate.append(
                {candidate: 0 for candidate in self.candidates})
            # For each ballot's candidate, add votes
            for freq, ballot in self.pairs:
                self.votes_per_candidate[i][ballot[i]] += freq

    def __calc_path_preference(self):
        """Computes paths' strengths for Schulze method."""
        # Create an iterable for candidates
        candidates = list(self.candidates)
        # Number of candidates
        n_candidates = len(candidates)
        for i in range(n_candidates):
            # Get candidate1
            candidate1 = candidates[i]
            for j in range(i + 1, n_candidates):
                # Get candidate2
                candidate2 = candidates[j]
                # Get strengths of candidate1 VS candidate2
                strength1 = self.__calc_strength(candidate1, candidate2)
                # Get strengths of candidate2 VS candidate1
                strength2 = self.__calc_strength(candidate2, candidate1)
                # Save strengths
                self.path_preference_graph[candidate1][candidate2] = strength1
                self.path_preference_graph[candidate2][candidate1] = strength2

    def __calc_strength(self, candidate1, candidate2):
        """
        The weakest link of the strongest path.
        Arguments:
            candidate1 -- origin candidate
            candidate2 -- destiny candidate
            (path from candidate1 to candidate2)
        """
        # Find possible paths between candidate1 and candidate2
        paths = self.__calc_paths(candidate1, candidate2)

        # Get strength for each path (weakest link)
        strength = list(map(min, paths))

        # Return the strongest strength
        return max(strength)

    def __calc_paths(self, candidate1, candidate2, candidates=None):
        """
        Computes the possible paths between candidate1 and candidate2.
        Arguments:
            candidate1 -- origin candidate
            candidate2 -- destiny candidate
            (path from candidate1 to candidate2)
        """
        # Check if candidates exists
        if candidates is None:
            candidates = self.candidates - {candidate1}
        paths = []  # list of possible paths
        path = []  # list of weights
        # For each candidate that is not candidate1...
        for candidate in candidates:
            # Get preference of candidate1 over candidate
            preference = self.net_preference_graph[candidate1][candidate]
            path.append(preference)  # save current weigth
            # End of path
            if candidate == candidate2:
                paths.append(path)  # add to possible paths
                path = []  # start a new path
            else:  # path isn't over
                new_candidates = candidates - {candidate}
                subpath = self.__calc_paths(candidate, candidate2,
                                            new_candidates)
                # For each subpath (list of weights),
                # concatenate with current path and save it
                for weights in subpath:
                    paths.append(path + weights)
        # Return a list of possible paths between candidate1 and candidate2
        return paths

    def _build_graph(self):
        """
        Build graph for Kemeny-Young method.
        An adaptation from:
        http://vene.ro/blog/kemeny-young-optimal-rank-aggregation-in-python.html
        """
        n_candidates = len(self.candidates)
        ranks = []
        for freq, ballot in self.pairs:
            for i in range(freq):
                ranks.append(list(ballot))
        ranks = np.array(ranks)
        edge_weights = np.zeros((n_candidates, n_candidates))
        for i, j in combinations(range(n_candidates), 2):
            preference = ranks[:, i] - ranks[:, j]
            h_ij = np.sum(preference < 0)  # prefers i to j
            h_ji = np.sum(preference > 0)  # prefers j to i
            if h_ij > h_ji:
                edge_weights[i, j] = h_ij - h_ji
            elif h_ij < h_ji:
                edge_weights[j, i] = h_ji - h_ij
        return edge_weights

    @classmethod
    def parse_voting_data(cls, file_path):
        if file_path[-3:] != "soi":
            raise EncodingWarning("The extension has to be .soi")
        pairs = []
        num_candidates: int | None = None
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line[0] == "#":
                    if "NUMBER ALTERNATIVES" in line:
                        # Parse lines like: "# NUMBER ALTERNATIVES: 379"
                        num_candidates = int(line.split(":")[1].strip())
                else:
                    num_voters, order = line.split(":")
                    ballot = tuple(order.strip().split(","))
                    pair = (num_voters, ballot)
                    pairs.append(pair)
        if not set:
            print("No votes found in file")
        return cls(pairs, num_candidates=num_candidates)

    @classmethod
    def ballot_box(cls, choices):
        """
        :param choices: a list of ranked candidates,
            i.e, [ (voter's 1 ranked candidates),
                   (voter's 2 ranked candidates),
                   (voter's 3 ranked candidates) ... ]
        :return: VotingProfile, a set of (number of votes, candidates ranked)
        """
        vote_counts = Counter(choices)
        pairs = [(count, choice) for choice, count in vote_counts.items()]
        return cls(set(pairs))

    def __str__(self):
        ballot_distribution = "Ballots:\n" + "\n".join(
            [f"\t{pair[0]} instances of ballot {pair[1]}" for pair in
             self.pairs])
        candidates = "Candidates:\n\t" + str(self.candidates)
        total_votes = "Total number of votes:\n\t" + str(self.total_votes)
        pref_graph = "Preference graph:\n\t" + str(self.net_preference_graph)
        return "\n".join(
            [ballot_distribution, candidates, total_votes, pref_graph])
