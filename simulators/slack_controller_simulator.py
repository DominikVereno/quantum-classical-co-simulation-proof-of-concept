import numpy as np

import mosaik_api

from power_system_components.slack_controller import SlackController

META = {
    'type': 'time-based', 
    'models': {
        'SlackController': {
            'public': True,
            'any_inputs': True,
            'params': [],
            'attrs': ["slack_power"]
        }
    }
}

class SlackControllerSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.time = 0

    def init(self, simulator_id, step_size=1, time_resolution=None):
        self.simulator_id = simulator_id
        self.step_size = step_size

        if time_resolution and float(time_resolution) != 1.0:
            raise ValueError(f"Simulator {self.simulator_id} only accepts a time resolution of 1.0, however, {time_resolution} was passed.")

        return self.meta
    
    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of Slack Controller.")
        
        self.eid = 'SlackController'
        self.controller_instance = SlackController()

        return [{'eid': self.eid, 'type': model}]
    
    def step(self, time, inputs, max_advance):
        self.time = time

        data = inputs[self.eid]["P"]
        value_vector = np.array(list(data.values()))

        self.controller_instance.power_injections = value_vector
        self.controller_instance.step()

        return self.time + self.step_size

    def get_data(self, outputs) -> dict:
        data = {'time': self.time}

        data[self.eid] = {"slack_power": self.controller_instance.slack_power}

        return data
            

