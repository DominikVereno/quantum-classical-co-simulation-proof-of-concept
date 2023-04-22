from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt
import networkx

from grid.grid_elements import Bus, Branch

from solver.power_flow_solver import PowerFlowSolver

class Grid:
    def __init__(self, grid_spec: dict, use_quantum_simulator: bool = True) -> None:
        self.buses    = self.__extract_buses   (grid_spec["bus"   ])
        self.branches = self.__extract_branches(grid_spec["branch"])
        self.elements = {**self.buses, **self.branches}

        self.graph = self.__construct_graph()

        incidence_matrix = self.__construct_incidence_matrix()
        line_admittances = self.__construct_line_admittances()
        self.power_flow_solver = PowerFlowSolver(line_admittances, incidence_matrix, use_quantum_simulator)
    
    def step(self) -> None:
        nodal_injection = self.__get_bus_power()
        
        line_flow = self.power_flow_solver.compute_line_flows(nodal_injection)

        self.__set_line_flow(line_flow)

    def draw(self) -> None:
        networkx.draw(self.graph, with_labels = True)
        plt.show()

    def __get_bus_power(self) -> np.array:
        return np.array([bus.P for bus in self.buses.values()])
    
    def __set_line_flow(self, line_flow: np.array) -> None:
        for idx, branch in enumerate(self.branches.values()):
            branch.P = line_flow[idx]

    def __extract_buses(self, bus_spec: list) -> OrderedDict:
        buses = OrderedDict()

        for bus_data in bus_spec:
            name = bus_data[0]
            buses[name] = Bus(name=name)
            
        return buses
    
    def __extract_branches(self, branch_spec: list) -> OrderedDict:
        branches = OrderedDict()

        for branch in branch_spec:
            branch_name = branch[0]

            from_bus_name = branch[1]
            to_bus_name   = branch[2]

            from_bus = self.buses[from_bus_name]
            to_bus   = self.buses[to_bus_name  ] 
             
            admittance = branch[3]
            branches[branch_name] = Branch(branch_name, from_bus, to_bus, admittance)
        
        return branches

    def __construct_graph(self) -> networkx.Graph:
        graph = networkx.Graph()

        for bus in self.buses.values():
            graph.add_node(bus.name)

        for branch in self.branches.values():
            graph.add_edge(branch.from_bus.name, branch.to_bus.name)
        
        return graph
    
    def __construct_incidence_matrix(self) -> np.array:
        incidence_matrix = np.zeros((len(self.branches), len(self.buses)))

        for branch_idx, branch in enumerate(self.branches.values()):
            from_index = self.__get_bus_index(branch.from_bus.name)
            to_index   = self.__get_bus_index(branch.to_bus  .name)

            incidence_matrix[branch_idx][from_index] =  1
            incidence_matrix[branch_idx][to_index  ] = -1

        return incidence_matrix
    
    def __construct_line_admittances(self) -> np.array:
        line_admittances = np.zeros(len(self.branches), dtype=np.cdouble)

        for branch_idx, branch in enumerate(self.branches.values()):
            line_admittances[branch_idx] = branch.admittance
    
        return line_admittances
    
    def __get_bus_index(self, bus_name_to_find) -> int:
        for idx, bus_name in enumerate(self.buses.keys()):
            if bus_name == bus_name_to_find:
                return idx
            
        raise IndexError()
