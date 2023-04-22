import mosaik_api

from grid.grid import Grid

META = {
    'type': 'time-based',
    'models': {
        'Grid': {
            'public': True,
            'params': ['grid_spec'],
            'attrs' : []
            },
        'Bus': {
            'public': False,
            'params': [],
            'attrs' : ['P'], # Active power [MW]
        },
        'Branch': {
            'public': False,
            'params': ['Y'], # Admittance [S] (complex-valued)
            'attrs' : ['P'], # Active power [MW]
        }
        
    }
}

class GridSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Grid-'
        self.grids = {}
        self.grids_by_grid_element = {}
        self.time = 0
    
    def init(self, simulator_id, use_quantum_simulator: bool = True, step_size=1, time_resolution=None):
        self.simulator_id    = simulator_id
        self.step_size       = step_size
        self.use_quantum_simulator = use_quantum_simulator
        
        if time_resolution and float(time_resolution) != 1.0:
            raise ValueError(f"Simulator {self.simulator_id} only accepts a time resolution of 1.0, however, {time_resolution} was passed.")

        return self.meta

    def create(self, number_of_grids, model, grid_spec):
        if(model != "Grid"):
            raise ValueError(f"Simulator {self.simulator_id} can only be used to create models of type Grid. Model type {model} was passed.")
    
        next_grid_index = len(self.grids)
        added_grids = []

        for index in range(next_grid_index, next_grid_index + number_of_grids):
            grid_info = self.__create_and_add_new_grid(index, grid_spec)
            added_grids.append(grid_info)
        
        return added_grids
    
    def step(self, time, inputs, max_advance):
        self.time = time

        for element_id, attributes in inputs.items():
            grid_id = self.grids_by_grid_element[element_id]
            grid_element_name = element_id[len(grid_id):]
            grid = self.grids[grid_id]
            grid_element = grid.elements[grid_element_name]
            
            for attribute_name, values in attributes.items():
                new_value = sum(values.values())
                setattr(grid_element, attribute_name, new_value)

        for grid_id, grid_instance in self.grids.items():
            if grid_id in inputs:
                self._process_grid_inputs(grid_instance, attributes = inputs[grid_id])

            grid_instance.step()
        
        return time + self.step_size
    
    def get_data(self, outputs):
        data = {'time': self.time}

        for entity_id, attributes in outputs.items():
            grid_id = self.grids_by_grid_element[entity_id]
            grid_element_name = entity_id[len(grid_id):]
            grid = self.grids[grid_id]
            grid_element = grid.elements[grid_element_name]

            data[entity_id] = {}

            for attribute in attributes:
                data[entity_id][attribute] = getattr(grid_element, attribute)
        
        return data

    def __create_and_add_new_grid(self, id_index, grid_spec) -> dict:
        grid_instace = Grid(grid_spec, use_quantum_simulator=self.use_quantum_simulator)
        grid_id = f"{self.eid_prefix}{id_index}"
        self.grids[grid_id] = grid_instace

        buses    = self.__add_bus_elements   (grid_id)
        branches = self.__add_branch_elements(grid_id)

        grid_info = {
            "eid"     : grid_id,
            "type"    : "Grid",
            "rel"     : [],
            "children": buses + branches
        }
        
        return grid_info
    
    def __add_bus_elements(self, grid_id) -> list:
        grid = self.grids[grid_id]

        added_buses = []
        for bus_name in grid.buses.keys():
            bus_eid = self.__grid_element_eid(grid_id, bus_name)
            self.grids_by_grid_element[bus_eid] = grid_id

            added_buses.append({
                'eid' : bus_eid,
                'type': 'Bus',
                'rel' : []
            })
        
        return added_buses
    
    def __add_branch_elements(self, grid_id) -> list:
        grid = self.grids[grid_id]

        added_branches = []
        for branch_name, branch in grid.branches.items():
            branch_eid = self.__grid_element_eid(grid_id, branch_name)
            self.grids_by_grid_element[branch_eid] = grid_id

            from_bus_eid = self.__grid_element_eid(grid_id, branch.from_bus.name)
            to_bus_eid   = self.__grid_element_eid(grid_id, branch.to_bus  .name)

            added_branches.append({
                'eid' : self.__grid_element_eid(grid_id, branch_name),
                'type': "Branch",
                'rel' : [from_bus_eid, to_bus_eid]
            })
        
        return added_branches
    
    def __grid_element_eid(self, grid_id, element_id):
        return f"{grid_id}{element_id}"
    
    def _process_grid_inputs(self, grid_instance, attributes):
        for attr, values in attributes.items():
            for source_eid, nodal_injection in values.items():
                print(f"{source_eid}: {nodal_injection}")
                grid_instance.nodal_injection = nodal_injection