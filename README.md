<a  name="_"></a>
# Computational Social Choice Toolkit [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Description
Toolkit to benchmark social choice rules. The toolkit supports the definition of voting rules as well as the generation voter populations.

## Code
- run.py:     Entry point. Run after setting up the num_candidates, num_voters, number_iterations, voters_models in main().
- models.py:  Defining voting models. Currently there are Random, Gaussian, and Dirichlet models.
- profile.py: All voting rules are defined and extended in class Profile.
- utils.py :  Rendering utils.

### Usage
```
python3.9 run.py [-h] [-v] num_candidates num_voters num_iterations voters_model
```

## Requirements
Python3.9, numpy, matplotlib, tqdm, pandas

## Licence & Copyright
This software was developed in the hope that it would be of some use to the agent research community, and is freely available for redistribution and/or modification under the terms of the GNU General Public Licence. It is distributed WITHOUT WARRANTY; without even the implied warranty of merchantability or fitness for a particular purpose. See the [GNU General Public License](https://github.com/raviq/Genon/blob/master/LICENCE.md) for more details.

If you find this code to be of any use, please let me know. I would also welcome any feedback.

Copyright (c) 2022 Rafik Hadfi, rafik.hadfi@gmail.com
