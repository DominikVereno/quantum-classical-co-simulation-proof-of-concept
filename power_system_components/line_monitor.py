import numpy as np

class LineMonitor:
    def __init__(self, limit) -> None:
        self.limit = limit

        self.line_flow = 0.0
        self.power_reduction = 0.0
        self.previous_reduction = self.power_reduction

    def step(self) -> None:
        if self.overflow_detected():
            self.power_reduction = np.absolute(np.absolute(self.line_flow) - self.limit) + self.previous_reduction*0.75
        else:
            self.power_reduction = 0.0
        
        self.previous_reduction = self.power_reduction

    def overflow_detected(self) -> bool:
        return np.absolute(self.line_flow) > self.limit    
    

    