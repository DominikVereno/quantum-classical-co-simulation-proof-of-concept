# Repository Contents

## Folders
- `data`: Contains data to configure the simulation. Most importantly, it contains the specification of the test grids, and the load and generation profiles. 
- `documentation`: Markdown files and images for documentation. 
- `grid`: Python file related to the power-grid simulation model. These files are agnostic to their use in a (Mosaik) co-simulation.
- `power_system_components`: Python files that specify the behavior of the simulated generators, consumers, etc. Similarly to the files in `grid`, they are agnostic to their use in a (Mosaik) co-simulation.
- `simulation_results`: Contains (a selection) of simulation results in the form of CSV files. The `result_analysis.ipynb` notebook is used to open, analyze, and illustrate their contents.
- `simulators`: Contains python classes that implement the Mosaik Simulator API. They interface the domain logic in `grid` and `power_system_components` with the Mosaik framework. This folder also contains `collector.py`, a simulator responsible for result logging. 
- `solver`: The directory includes code for running power-flow analysis and the quantum algorithm for solving linear systems of equations.
    - `power_flow_solver.py`: Quantum power flow implementation.
    - `hhl_solver.py`: Contains an implementation of the [HHL algorithm](https://arxiv.org/abs/0811.3171). The code is based on the work by [Sævarsson et al.](https://arxiv.org/abs/2204.14028) 

## Files
- `result_analysis.ipynb`: Experimental notebook for analyzing the simulation results. The notebook is used to create figures (e.g. for publications). 
- `scenario.py`: The specification of the co-simulation scenario. Here, the simulation units and their connections are defined. T
- `simulation.py`: The script instatiates and runs the co-simulation scenario.
