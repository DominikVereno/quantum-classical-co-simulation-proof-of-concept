import mosaik_api

from power_system_components.aggregated_load import AggregatedLoad

META = {
    'type': 'time-based',
    'models': {
        'AggregatedLoad': {
            'public': True,
            'params': ['max_power'],
            'attrs' : ['P']
        }
    }
}

class AggregatedLoadSim(mosaik_api.Simulator):
    def __init__(self) -> None:
        super().__init__(META)
        self.model_name = list(self.meta['models'].keys())[0]
        self.eid_prefix = f'{self.model_name}-'
        self.loads = {}
        self.time = 0

    def init(self, simulator_id, step_size=1, time_resolution=None, eid_prefix=None):
        self.simulator_id = simulator_id
        self.step_size = step_size

        if time_resolution and float(time_resolution) != 1.0:
            raise ValueError(f"Simulator {self.simulator_id} only accepts a time resolution of 1.0, however, {time_resolution} was passed.")

        if eid_prefix:
            self.eid_prefix = eid_prefix

        return self.meta
    
    def create(self, number_of_loads, model, max_power):
        if model != self.model_name:
            raise ValueError(f"Simulator {self.simulator_id} can only be used to create models of type {self.model_name}. Model type {model} was passed.")

        next_index = len(self.loads)
        new_loads = []

        for index in range(next_index, next_index + number_of_loads):
            load_descr = self.__create_and_add_new_load(index, max_power)
            new_loads.append(load_descr)
        
        return new_loads
    
    def step(self, time, inputs, max_advance) -> int:
        self.time = time

        self.__step_all_loads()

        return time + self.step_size
    
    def get_data(self, outputs) -> dict:
        data = {'time': self.time}

        for load_id, attributes in outputs.items():
            data[load_id] = self.__extract_attributes_from_load(load_id, attributes)
        
        return data

    def __create_and_add_new_load(self, id_index, max_power) -> dict:
        load = AggregatedLoad(max_power=max_power)
        load_id = f"{self.eid_prefix}{id_index}"
        self.loads[load_id] = load

        return {'eid': load_id, 'type': self.model_name}
    
    def __step_all_loads(self) -> None:
        for load in self.loads.values():
            load.step(time=self.time)

    def __extract_attributes_from_load(self, load_id, attributes) -> dict:
        load_data = {}
            
        load = self.loads[load_id]
        for attribute in attributes:
            if self.__is_load_attribute(attribute_name=attribute):
                load_data[attribute] = getattr(load, attribute)
            else:
                raise ValueError(f"Unknonw attribute")
            
        return load_data
    
    def __is_load_attribute(self, attribute_name) -> bool:
        return attribute_name in self.meta['models'][self.model_name]['attrs']