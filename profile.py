"""
Voting profiles
"""

import sys
import numpy as np
from itertools import combinations

sys.setrecursionlimit(1000000)

class Profile():
    """
    Profile is a tuple (number of votes, ballot) with the umber
    of times the vote occurs and the corresponding ballot defined
    as some ordering of the candidates.
    For instance:
        votes = Profile({(17, (1,3,2,0)), (40, (3,0,1,2)), (52, (1,0,2,3))})
    means 17 people like candidate 1 the most, then candidate 3 in the second
    position, then candidate 2 in the third position, and so on.

    Properties:
        pairs -- set of (number of votes, ballot)
        candidates -- candidates in ballots
        total_votes -- total number of votes
        net_preference_graph -- represents the preference net
        votes_per_candidate -- total votes for each candidate
    """
    def __init__(self, pairs):
        """
        Init the profile.
        Arguments: pairs -- a set of votes and candidates
        """
        # Set the pairs
        self.pairs = pairs
        # Get the candidates from pairs
        # iter -- transform the set into an iterable
        it = iter(pairs)
        # next -- get the next from the iterable
        pair = next(it)
        # [1] -- candidates' index ([0] is #votes index)
        candidates = pair[1]
        # set -- convert to a set
        self.candidates = set(candidates)
        # Get the votes
        votes = [n_votes for n_votes, _ in pairs]
        # Get total number of votes
        self.total_votes = sum(votes)
        # Create a Net Preference Graph
        self.__calc_net_preference()
        # Set votes_per_candidate for Plurality
        self.__calc_votes_per_candidate()
        # Initialize a Path Preference Graph
        self.path_preference_graph = {candidate: dict() for candidate in self.candidates}

    #---------------------------------------------
    # Comparison routines
    #---------------------------------------------
    def net_preference(self, candidate1, candidate2):
        """
        Computes preference between 2 candidates according to
        the Net Preference Graph and returns its answer
        Arguments:
        candidate1 -- candidate to be compared
        candidate2 -- other candidate to be compared
        """
        # Get the preference in the graph
        return self.net_preference_graph[candidate1][candidate2]

    def does_pareto_dominate(self, candidate1, candidate2):
        """
        Returns True when candidate1 is preferred in all ballots.
        False, otherwise.
        Arguments:
        candidate1 -- candidate to be compared
        candidate2 -- other candidate to be compared
        """
        # A boolean list as candidate1 preferred
        preferred = [b.index(candidate1) < b.index(candidate2) for _, b in self.pairs]
        # Apply AND in all elements
        return all(preferred)

    def ranking(self, scorer):
        """
        Returns a set of candidate winners according to some score function
        Arguments:
        scorer -- score function (ex.: borda, copeland)
        """
        # A list of (candidate, score)
        scores = self.score(scorer)
        # Ranking is the score list ordered by score descrescent
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def score(self, scorer):
        """
        Returns a set of candidate according to some score function.
        Arguments:
        scorer -- score function (ex.: borda, copeland)
        """
        # A list of (candidate, score)
        scores = [(candidate, scorer(candidate)) for candidate in self.candidates]
        # Ranking is the score list ordered by candidate id crescent
        scores.sort(key=lambda x: x[0])
        return scores

    def winners(self, scorer):
        """
        Returns a set of candidate winners according to some score function
        Arguments:
        scorer -- score function (ex.: borda, copeland)
        """
        ranking = self.ranking(scorer)  # get ranking
        best_score = ranking[0][1]      # get best score first tuple in ranking
        # Filter ranking to get all best score
        bests = list(filter(lambda x: x[1] == best_score, ranking))
        # Get only the candidates
        winners, scores = zip(*bests)
        # Return a set of winners
        return set(winners)

    def __preference(self, n_votes, i, j):
        """
        Computes the preference between 2 candidates and returns
        the preference according to the number of votes.
        Arguments:
        n_votes -- number of votes
        i -- index of one candidate
        j -- index of the other candidate
        """
        # Difference between candidates
        n = i - j
        # Exception: if n is equal to 0, preference is 0,
        # i.e, candidates with same index
        if n == 0:
            return 0
        # Preference is n_votes * n / abs(n)
        return n_votes * np.sign(n)

    def __calc_net_preference(self):
        """ Create a Net Preference Graph. """
        # Create an iterable for candidates
        candidates = list(self.candidates)
        # Number of candidates
        n_candidates = len(candidates)
        # Initialize graph
        self.net_preference_graph = {candidate: dict() for candidate in candidates}
        for i in range(n_candidates):
            # Get candidate1
            candidate1 = candidates[i]
            for j in range(i, n_candidates):
                # Get candidate2
                candidate2 = candidates[j]
                # Preference list
                preferences = list()
                # For each pair of voting
                for n_votes, ballot in self.pairs:
                    k = ballot.index(candidate2)              # get the index of candidate2
                    m = ballot.index(candidate1)              # get the index of candidate1
                    p = self.__preference(n_votes, k, m)  # Computes the preference
                    preferences.append(p)                 # save preference
                # Computes the preference
                preference = sum(preferences)
                # Save preferences
                self.net_preference_graph[candidate1][candidate2] = preference   # candidate1 VS candidate2
                self.net_preference_graph[candidate2][candidate1] = -preference  # candidate2 VS candidate1

    def __calc_votes_per_candidate(self):
        """Computes total votes per each candidate for each rank position"""
        # Initialize structure to save the scores
        self.votes_per_candidate = list()
        # Number of candidate
        n_candidates = len(self.candidates)
        # For each candidate
        for i in range(n_candidates):
            self.votes_per_candidate.append({candidate: 0 for candidate in self.candidates})
            # For each ballot's candidate, add votes
            for n_votes, ballot in self.pairs:
                self.votes_per_candidate[i][ballot[i]] += n_votes

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
                # Get strengths
                strength1 = self.__calc_strength(candidate1, candidate2)  # candidate1 VS candidate2
                strength2 = self.__calc_strength(candidate2, candidate1)  # candidate2 VS candidate1
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
        strength = list(map(lambda x: min(x), paths))

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
        n_candidates = len(candidates)  # number of candidates
        paths = list()          # list of possible paths
        path = list()           # list of weights
        # For each candidate that is not candidate1...
        for candidate in candidates:
            # Get preference of candidate1 over candidate
            preference = self.net_preference_graph[candidate1][candidate]
            path.append(preference)  # save current weigth
            # End of path
            if candidate == candidate2:
                paths.append(path)       # add to possible paths
                path = list()            # start a new path
            else: # path isn't over
                new_candidates = candidates - {candidate}
                subpath = self.__calc_paths(candidate, candidate2, new_candidates)
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
        n_voters = self.total_votes
        n_candidates = len(self.candidates)
        ranks = list()
        for n_votes, ballot in self.pairs:
            for i in range(n_votes):
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
    def ballot_box(cls, choices):
        """
        Index and order choices for Profile.
        Arguments:
            choices -- a list of ranked candidates,
            i.e, [ [voter's 1 ranked candidates],
                   [voter's 2 ranked candidates],
                   [voter's 3 ranked candidates] ... ]
        Return type:
            A set of (number of votes, candidates ranked)
        """
        n_voters = len(choices)  # number of voters
        if not (type(choices[0][0]) is tuple): # it's not indexed
            # INDEX CHOICES, i.e., name candidates
            # For each classification, create [(candidate1, rank1), (candidate2, rank2)...]
            choices = list(map(lambda x: list(enumerate(x)), choices))
        # ORDER each classification in decrescent order
        choices = list(map(lambda x: sorted(x, key=lambda y: y[1], reverse=True), choices))
        # GROUP choices with same ordering (same preference order)
        # Empty dict for save pairs -> {'preference order': number of voters}
        ballots = dict()
        # For each classification...
        for i in range(n_voters):
            key, _ = zip(*choices[i])  # get only candidates' names as key
            key = tuple(key)           # cast to tuple to use as dict's key
            # Counts the classifications with same ordering
            ballots[key] = ballots.get(key, 0) + 1
        # DATA FOR PROFILE
        # Pairs -> [(ballot, number of votes)...]
        pairs = list(ballots.items())
        # Transform -> [(number of votes, ballot)...]
        pairs = list(map(lambda x: (x[1], x[0]), pairs))
        # Cast to set and return as a Profile
        return cls(set(pairs))

    @classmethod
    def aggr_rank(cls, probabilities, sc_functions, predictions=[]):
        """Aggregate probabilities and return a ranking.
        Arguments:
            probabilities -- a list of instances' probabilities,
                i.e, [ [voter's 1 instances' probabilities],
                       [voter's 2 instances' probabilities],
                       [voter's 3 instances' probabilities] ... ]
            sc_functions -- a list with the name of social choice functions
            predictions -- a list of instances' predictions (default []),
                i.e, [ [voter's 1 instances' predictions],
                       [voter's 2 instances' predictions],
                       [voter's 3 instances' predictions] ... ]
        """
        profile = cls.ballot_box(probabilities)
        rankings = dict()
        for scf in sc_functions:
            if scf == 'plurality':
                rank = profile.plurality(probabilities, predictions)
            elif scf == 'kemeny_young':
                rank = profile.kemeny_young()
            else:
                rank = profile.score(eval('profile.' + scf))
            rankings[scf] = rank
        return rankings

    def show(self):
        print ("Ballots : ")
        for p in self.pairs:
            print ("     {} instances of ballot {}".format(*p))
        print (" Candidates : ", self.candidates)
        print (" Total number of votes : ", self.total_votes)
        print (" Preference graph :", self.net_preference_graph)
