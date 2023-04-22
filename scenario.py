import mosaik
import mosaik.util

from data.test_grids import grid_5bus

SIM_CONFIG = {
    'GridSim': {
        'python': 'simulators.grid_simulator:GridSim'
    },
    'SolarFarmSim': {
        'python': 'simulators.solar_farm_simulator:SolarFarmSim'
    },
    'AggregatedLoadSim': {
        'python': 'simulators.aggregated_load_simulator:AggregatedLoadSim'
    },
    'SlackGeneratorSim': {
        'python': 'simulators.slack_generator_simulator:SlackGeneratorSim'
    },
    'SlackControllerSim': {
        'python': 'simulators.slack_controller_simulator:SlackControllerSim'
    },
    'LineMonitorSim': {
        'python': 'simulators.line_monitor_simulator:LineMonitorSim'
    },
    'Collector': {
        'python': 'simulators.collector:Collector'
    }
}

class Grid():
    def __init__(self, grid_elements) -> None:
      self.grid_elements = grid_elements

    def __getitem__(self, key):
       return next(element for element in self.grid_elements if key in element.eid)

class Scenario:
    def __init__(self, simulation_duration, use_quantum_simulator:bool=True, grid_spec=grid_5bus, result_logging:bool=True) -> None:
        self.simulation_duration = simulation_duration
        self.use_quantum_simulator = use_quantum_simulator
        self.grid_spec = grid_spec
        self.result_logging = result_logging

        self.world = mosaik.World(SIM_CONFIG)

        self.__start_all_simulators()
        self.__instantiate_all_entities()
        self.__connect_entities()
        self.__connect_entities_to_collector()
    
    def run(self) -> None:
        self.world.run(until=self.simulation_duration)

    def __start_all_simulators(self) -> None:
        self.grid_sim            = self.world.start('GridSim', use_quantum_simulator=self.use_quantum_simulator)
        self.solar_farm_sim      = self.world.start('SolarFarmSim')
        self.aggregated_load_sim = self.world.start('AggregatedLoadSim')
        self.slack_gen_sim       = self.world.start('SlackGeneratorSim')
        self.slack_contrl_sim    = self.world.start('SlackControllerSim')
        self.line_monitor_sim    = self.world.start('LineMonitorSim')
        self.collector_sim       = self.world.start('Collector', persist_data=self.result_logging, log_file_suffix = "SIM" if self.use_quantum_simulator else "REAL")

    def __instantiate_all_entities(self) -> None:
        grid_elements = self.grid_sim.Grid(grid_spec=self.grid_spec).children
        self.grid = Grid(grid_elements=grid_elements)

        self.solar_farm = self.solar_farm_sim     .SolarFarm     (max_power=3.0)
        self.load_bus3  = self.aggregated_load_sim.AggregatedLoad(max_power=0.5)
        self.load_bus4  = self.aggregated_load_sim.AggregatedLoad(max_power=0.5)
        self.load_bus5  = self.aggregated_load_sim.AggregatedLoad(max_power=1.5)
        self.slack_gen  = self.slack_gen_sim      .SlackGenerator()

        self.slack_contrl = self.slack_contrl_sim.SlackController()
        self.line_monitor = self.line_monitor_sim.LineMonitor(limit=2.0)

        self.collector_sim = self.collector_sim.Monitor()

    def __connect_entities(self) -> None:
        for load in [self.solar_farm, self.load_bus3, self.load_bus4, self.load_bus5]:
            self.world.connect(load, self.slack_contrl, "P")

        self.world.connect(self.slack_contrl, self.slack_gen, ("slack_power", "slack_demand"))
        self.world.connect(self.solar_farm , self.grid["Bus2"], 'P')

        self.world.connect(self.load_bus3, self.grid["Bus3"], 'P')
        self.world.connect(self.load_bus4, self.grid["Bus4"], 'P')
        self.world.connect(self.load_bus5, self.grid["Bus5"], 'P')

        self.world.connect(self.grid["Branch1-2"], self.line_monitor, ('P', 'line_flow'))
        self.world.connect(self.line_monitor, self.solar_farm, 'power_reduction', time_shifted=True, initial_data={'power_reduction': 0.0})

    def __connect_entities_to_collector(self):
        self.__connect_to_collector(self.grid["Branch1-2"], "P")
        self.__connect_to_collector(self.line_monitor, "power_reduction")
        self.__connect_to_collector(self.slack_gen, "P")

    def __connect_to_collector(self, entitiy, attribute) -> None:
        self.world.connect(entitiy, self.collector_sim, attribute)

