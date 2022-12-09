<a  name="_"></a>
# Computational Social Choice Toolkit [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Description

This is a Python toolkit for the study of voting rules used in [computational social choice theory](https://en.wikipedia.org/wiki/Computational_social_choice). The toolkit allows you to programatically define the `voting rules` as well as the distributions of the voters, defined as `voter models`. This is illustrated below.

<img src="./figures/Overview.png" style="height:50%; width:50%"/>


### Voting rules
Our voting rules are defined in terms of socres. That is, the rule takes a candidate and returns its score. The obtained scores for all of the candidates could then be used to determine the winner(s). For instance, the `Borda` score is implemented as following.

```python
    def borda(self, candidate):
        # Max score to be applied with borda count
        top_score = len(self.candidates) - 1
        # Get pairwise scores
        scores = [n_votes * (top_score - ballot.index(candidate)) for n_votes, ballot in self.pairs]
        # Return the total score
        return sum(scores)
```
Other scores are defined in 'profile.py'.

### Voter Models
In general, voters rank the candidates according to ordinal preferences that are often defined as permutations over the set of candidates. Such preference could be defined in different ways. In the following we defined them according to 3 methods.
1. Random Preferences: each voter is assigned a random permutation over the set of candidates.
2. Gaussian distribution of the votes: the votes of the voters are normally distributed
3. Dirichlet-Multinomial distribution of the votes 

## Files

The main files of the package are:
| File | Description |
| ---- | --- |
| [**run.py**](./run.py) | This is the main entry point. Takes the number of candidates `num_candidates`, the number of voters `num_voters`, the number of trials to run `number_iterations`, and the model `voters_model` to generate the voters' population. |
| [**models.py**](./models.py) | Defining the models to adopt when generating the popuations of the voters. There are currently Random, Gaussian, and Multinomial-Dirichlet models. |
| [**profile.py**](./profile.py) | All voting rules are defined and extended in the `Profile` class. |
| [**utils.py**](./utils.py) |  Rendering utils. |

### Usage
```
python3.9 run.py [-h] [-v] num_candidates num_voters num_iterations voters_model
```
### Examples

To run 10 trials with `Dowdall`, `Simpson`, `Copeland`, and `Borda` rules for 5 candidates and 100 voters with random votes, run the command:
```
python3.9 run.py 5 100 10 "random"
```
The visual result is generated in `figures/scores_random.png`

<img src="./figures/scores_random.png" style="height:50%; width:50%"/>
 
## Dependencies
* Python3.9
* Numpy
* Matplotlib
* Pandas
* [Tqdm](https://github.com/tqdm/tqdm)

## Licence & Copyright
This software was developed in the hope that it would be of some use to the agent research community, and is freely available for redistribution and/or modification under the terms of the GNU General Public Licence. It is distributed WITHOUT WARRANTY; without even the implied warranty of merchantability or fitness for a particular purpose. See the [GNU General Public License](https://github.com/raviq/Genon/blob/master/LICENCE.md) for more details.

If you find this code to be of any use, please let me know. I would also welcome any feedback.

Copyright (c) 2022 Rafik Hadfi, rafik.hadfi [at] gmail [dot] com
