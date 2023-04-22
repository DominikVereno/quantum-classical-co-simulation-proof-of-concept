class SlackGenerator:
    def __init__(self) -> None:
        self.slack_demand = 0.0
        self.P = 0.0

    def step(self):
        self.P = -self.slack_demand