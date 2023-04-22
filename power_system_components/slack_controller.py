import numpy as np

class SlackController:
    def __init__(self) -> None:
        self.power_injections = None
        self.slack_power = 0.0

    def step(self) -> None:
        if self.power_injections is None:
            self.slack_power = 0.0
        else:
            self.slack_power = np.sum(self.power_injections)
