<a  name="_"></a>
# Computational Social Choice Toolkit [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Description
Toolkit to run and and benchmark social choice rules. The toolkit supports the definition of voting rules as well as the generation of different populations of voters.

## Files



| File | Description |
| ---- | --- |
| [**run.py**](./run.py) | This is the main entry point. Takes the `num_candidates`, `num_voters`, `number_iterations`, voters_models arguments in main()  |
| [**models.py**](./models.py) | Defining the models to adopt when generating the popuations of the voters. There are currently Random, Gaussian, and Dirichlet models. |
| [**profile.py**](./profile.py) | All voting rules are defined and extended in the `Profile` class. |
| [**utils.py**](./utils.py) |  Rendering utils. |

### Usage
```
python3.9 run.py [-h] [-v] num_candidates num_voters num_iterations voters_model
```
### Examples

In order to run 10 trials for Dowdall, Simpson, Copeland, and Borda rules for 5 candidates and 100 voters generated with random ballots run the command
```
python3.9 run.py 5 100 10 "random"
```
The visual result is genrated in `figures/scores_random.png`

![RandRule](figures/scores_random.png)
 
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
