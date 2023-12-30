# Quantum–classical co-simulation proof of concept

Study on the feasibility and obstacles of integrating a quantum computing–based simulator with a smart grid co-simulation 

For academic or technical questions and comments, please feel free to reach out to Dominik Vereno via e-mail: [dominik.vereno@fh-salzburg.ac.at](mailto:dominik.vereno@fh-salzburg.ac.at).

## Getting Started 

### Setup and Dependencies
After cloning the code, [create a virtual environment](https://realpython.com/lessons/creating-virtual-environment/), activate it, and then install all dependencies listed in `requirements.txt`. 

```
pip install -r requirements.txt
```
> **Note:** If you do not name your virtual environment `venv`, remember to add your virtual-environment path to the `.gitignore`.

### Executing and configuring the simulation
You can execute the simulation by running the `simulation.py` python script. The most important settings you can change without going to much into the code are:
- `simulation_duration`: Choose a number of timesteps for the simulation to run. Each time step represents a 15-minute interval. The duration should not exceed the length of the time series defined in `data/load_profiles.py`.
- `use_quantum_simulator`: A boolean flag to specify whether a simulated quantum computer is used or a real one. Beware of the long queuing times when running on real hardware.
- `result_logging`: If set to `True`, a log file while be created in the `simulation_results/` directory. Otherwise, the simulation data will only be displayed in the console. 

## Repository Contents
This respository represents an active research project and not a ready-to-ship software tool. Therefore, you'll find various types of files: code scripts, data-definition files, and simulation results. 

Refer to [Repository Contents](documentation/repository_contents.md) for detailed information. 

## Citation
> This section is not finished. 

Please use the following `bib` entry when citing this work: 

```
@article{Vereno2023,
  title = {Quantum–classical co-simulation for smart grids: a proof-of-concept study on feasibility and obstacles},
  volume = {6},
  ISSN = {2520-8942},
  url = {http://dx.doi.org/10.1186/s42162-023-00292-1},
  DOI = {10.1186/s42162-023-00292-1},
  number = {S1},
  journal = {Energy Informatics},
  publisher = {Springer Science and Business Media LLC},
  author = {Vereno,  Dominik and Khodaei,  Amin and Neureiter,  Christian and Lehnhoff,  Sebastian},
  year = {2023},
  month = oct 
}
```
