from scenario import Scenario

def main():
    sim_scenario = Scenario(simulation_duration=32, use_quantum_simulator=False, result_logging=True)
    sim_scenario.run()

if __name__ == "__main__":
    main()