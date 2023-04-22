import mosaik_api

from power_system_components.solar_farm import SolarFarm

META = {
    'type': 'time-based',
    'models': {
        'SolarFarm': {
            'public': True,
            'params': ['max_power'],
            'attrs' : ['P', 'power_reduction']
        }
    }
}

class SolarFarmSim(mosaik_api.Simulator):
    def __init__(self) -> None:
        super().__init__(META)
        self.model_name = list(self.meta['models'].keys())[0]
        self.eid_prefix = f'{self.model_name}-'
        self.farms = {}
        self.time = 0
    
    def init(self, simulator_id, step_size=1, time_resolution=None, eid_prefix=None):
        self.simulator_id = simulator_id
        self.step_size = step_size

        if time_resolution and float(time_resolution) != 1.0:
            raise ValueError(f"Simulator {self.simulator_id} only accepts a time resolution of 1.0, however, {time_resolution} was passed.")

        if eid_prefix:
            self.eid_prefix = eid_prefix

        return self.meta
    
    def create(self, number_of_farms, model, max_power):
        if model != self.model_name:
            raise ValueError(f"Simulator {self.simulator_id} can only be used to create models of type {self.model_name}. Model type {model} was passed.")

        next_index = len(self.farms)
        new_farms = []

        for index in range(next_index, next_index + number_of_farms):
            farm_descr = self.__create_and_add_new_farm(index, max_power)
            new_farms.append(farm_descr)
        
        return new_farms
    
    def step(self, time, inputs, max_advance) -> int:
        self.time = time

        for farm_index, farm in self.farms.items():
            if farm_index in inputs:
                power_reduction = sum(inputs[farm_index]["power_reduction"].values())
                farm.power_reduction = power_reduction
            farm.step(time=self.time)

        return time + self.step_size
    
    def get_data(self, outputs) -> dict:
        data = {'time': self.time}

        for farm_id, attributes in outputs.items():
            data[farm_id] = self.__extract_attributes_from_farm(farm_id, attributes)
        
        return data
    
    def __create_and_add_new_farm(self, id_index, max_power) -> dict:
        farm = SolarFarm(max_power=max_power)
        farm_id = f"{self.eid_prefix}{id_index}"
        self.farms[farm_id] = farm

        return {'eid': farm_id, 'type': self.model_name}
        

    def __extract_attributes_from_farm(self, farm_id, attributes) -> dict:
        farm_data = {}
            
        farm = self.farms[farm_id]
        for attribute in attributes:
            if self.__is_farm_attribute(attribute_name=attribute):
                farm_data[attribute] = getattr(farm, attribute)
            else:
                raise ValueError(f"Unknonw attribute")
            
        return farm_data

    def __is_farm_attribute(self, attribute_name) -> bool:
        return attribute_name in self.meta['models'][self.model_name]['attrs']