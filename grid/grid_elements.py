from typing import Union
import numpy as np

FLOAT = Union[float, np.floating]

class GridElement:
    def __init__(self, name: str) -> None:
        self.name = name

class Bus(GridElement):
    def __init__(self, name: str) -> None:
        super().__init__( name)
        self.P = 0.0

class Branch(GridElement):
    def __init__(self, name: str, from_bus: Bus, to_bus: Bus, admittance: FLOAT ) -> None:
        super().__init__(name)
        self.from_bus = from_bus
        self.to_bus   = to_bus
        
        self.admittance = admittance
        self.P = 0.0
