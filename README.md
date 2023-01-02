# Optimisation for Production Figures

## Core Packages
### part2.py
This is the core package for all the algorithm. Higher-level wrappers are also defined here and will be called directly by the run scripts.
### part2_util.py
This is the supplementary utilities to support the functionality of part2.py. This includes the user-defined initialisation point.
### part2_class.py
The class with the information (distance, capacity, cost) is being contained in this file. The class will be called in part2.py.

## Run Scripts
run_script.py
Script to run optimisation using  the Monte Carlo Method.

run_st_script.py
Script to run optimisation using the Hooke-Jeeves and Simple Local Search methods.

run_sa_script.py
Script to run optimisation using the Simulated Annealing method.

## Output
The program will save the output to file starting with _Output-xxx.csv_, whereby xxx refers to the optimisation algorithm. The file will be saved in the same directory.

## Running the script
Typically users do not interact with the underlying code directly. In order to run the optimisation, simple run the script files as shown below:
```
>python3 run_script.py
```

## Requirements
Vanilla Python 3.10 and numpy package
