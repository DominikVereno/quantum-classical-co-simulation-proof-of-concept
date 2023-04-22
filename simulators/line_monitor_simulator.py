import mosaik_api

from power_system_components.line_monitor import LineMonitor

META = {
    'type': 'time-based',
    'models': {
        'LineMonitor': {
            'public': True,
            'params': ['limit'],
            'attrs': ['line_flow', 'power_reduction']
        }
    }
}

class LineMonitorSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'LineMonitor-'
        self.monitors = {}
        self.time = 0

    def init(self, simulator_id, step_size=1, time_resolution=None, eid_prefix=None):
        self.simulator_id = simulator_id
        self.step_size = step_size

        if time_resolution and float(time_resolution) != 1.0:
            raise ValueError(f"Simulator {self.simulator_id} only accepts a time resolution of 1.0, however, {time_resolution} was passed.")

        if eid_prefix:
            self.eid_prefix = eid_prefix

        return self.meta
    
    def create(self, number_of_monitors, model, limit):
        if model != "LineMonitor":
            raise ValueError(f"Simulator {self.simulator_id} can only be used to create models of type LineMonitor. Model type {model} was passed.")

        next_index = len(self.monitors)
        new_monitors = []

        for index in range(next_index, next_index + number_of_monitors):
            monitor_descr = self.__create_and_add_new_monitor(index, limit)
            new_monitors.append(monitor_descr)

        return new_monitors

    def step(self, time, inputs, max_advance) -> int:
        self.time = time

        for monitor_id, monitor in self.monitors.items():
            if monitor_id in inputs:
                line_flow = sum(inputs[monitor_id]["line_flow"].values())
                monitor.line_flow = line_flow
            
            monitor.step()

        return time + self.step_size
    
    def get_data(self, outputs) -> dict:
        data = {'time': self.time}

        for monitor_id, attributes in outputs.items():
            data[monitor_id] = self.__extract_attributes_from_monitor(monitor_id, attributes)
        
        return data

    def __create_and_add_new_monitor(self, id_index, limit) -> dict:
        monitor = LineMonitor(limit)
        monitor_id = f"{self.eid_prefix}{id_index}"
        self.monitors[monitor_id] = monitor

        return {'eid': monitor_id, 'type': 'LineMonitor'}
    
    def __extract_attributes_from_monitor(self, monitor_id, attributes) -> dict:
        monitor_data = {}

        monitor = self.monitors[monitor_id]
        for attribute in attributes:
            if self.__is_monitor_attribute(attribute_name=attribute):
                monitor_data[attribute] = getattr(monitor, attribute)
            else:
                raise ValueError(f"Unkown attribute")
        
        return monitor_data
    
    def __is_monitor_attribute(self, attribute_name) -> bool:
        return attribute_name in self.meta['models']['LineMonitor']['attrs']