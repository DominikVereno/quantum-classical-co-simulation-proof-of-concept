from data.load_profiles import LOAD_CONSUMPTION

class AggregatedLoad:
    def __init__(self, max_power):
        self.max_power = max_power
        self.P = 0.0

    def step(self, time: int):
        try:
            consumption = LOAD_CONSUMPTION[time] * self.max_power
        except IndexError:
            print(f"The time must be in the range of [, {len(LOAD_CONSUMPTION)-1}]. Time passed was {time}.")
            
        self.P = -consumption