import mosaik_api

from power_system_components.slack_generator import SlackGenerator

META = {
    'type': 'time-based', 
    'models': {
        'SlackGenerator': {
            'public': True,
            'params': [],
            'attrs': ["slack_demand", "P"]
        }
    }
}

class SlackGeneratorSim(mosaik_api.Simulator):
    def __init__(self) -> None:
        super().__init__(META)
        self.eid_prefix = 'SlackGenerator-'
        self.generators = {}
        self.time = 0

    def init(self, simulator_id, step_size=1, time_resolution=None, eid_prefix=None):
        self.simulator_id = simulator_id
        self.step_size = step_size

        if time_resolution and float(time_resolution) != 1.0:
            raise ValueError(f"Simulator {self.simulator_id} only accepts a time resolution of 1.0, however, {time_resolution} was passed.")

        if eid_prefix:
            self.eid_prefix = eid_prefix

        return self.meta
    
    def create(self, number_of_generators, model):
        if model != "SlackGenerator":
            raise ValueError(f"Simulator {self.simulator_id} can only be used to create models of type SlackGenerator. Model type {model} was passed.")
        
        next_index = len(self.generators)
        new_generators = []

        for index in range(next_index, next_index + number_of_generators):
            generator_descr = self.__create_and_add_new_generator(index)
            new_generators.append(generator_descr)
        
        return new_generators
    
    def step(self, time, inputs, max_advance) -> int:
        self.time = time

        for generator_id, generator in self.generators.items():
            if generator_id in inputs:
                attributes = inputs[generator_id]
                for attribute, values in attributes.items():
                    setattr(generator, attribute, sum(values.values()))
            
            generator.step()
        
        return time + self.step_size

    def get_data(self, outputs) -> dict:
        data = {'time': self.time}

        for generator_id, attributes in outputs.items():
            data[generator_id] = self.__extract_attributes_from_generator(generator_id, attributes)
        
        return data

    def __create_and_add_new_generator(self, id_index) -> dict:
        generator = SlackGenerator()
        generator_id = f"{self.eid_prefix}{id_index}"
        self.generators[generator_id] = generator

        return {'eid': generator_id, 'type': 'SlackGenerator'}
    
    def __extract_attributes_from_generator(self, generator_id, attributes) -> dict:
        generator_data = {}

        generator = self.generators[generator_id]
        for attribute in attributes:
            if self.__is_generator_attribute(attribute):
                generator_data[attribute] = getattr(generator, attribute)
            else:
                raise ValueError(f"Unkown attribute")
        
        return generator_data
    
    def __is_generator_attribute(self, attribute_name) -> bool:
        return attribute_name in self.meta['models']['SlackGenerator']['attrs']